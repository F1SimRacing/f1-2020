import ctypes
import numbers
import socket

from f1_2020_telemetry.packets import unpack_udp_packet, PackedLittleEndianStructure
import logging

from f1_2020_telemetry.types import TeamIDs

from cassandra.telemetry.constants import PACKET_MAPPER

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


class Feed:
    def __init__(self, port: int = None):
        if not port:
            port = 20777

        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind(("", port))

    def get_latest(self):
        packet = unpack_udp_packet(self.socket.recv(2048))
        if not packet:
            return None, None

        try:
            user, teammate = format_packet_v2(packet)
        except:
            return None, None
        return user, teammate


def format_packet_v2(packet):
    packet_type = type(packet)
    players_car = packet.header.playerCarIndex

    # usually this is data about other players cars.
    if packet_type.__name__ not in PACKET_MAPPER.keys():
        return

    result = {
        "type": packet_type.__name__,
        "name": PACKET_MAPPER[packet_type.__name__],
        "sessionTime": packet.header.sessionTime,
        "sessionUID": int(packet.header.sessionUID),
    }

    if hasattr(packet, "participants"):
        team_id = packet.participants[19].teamId
        team_name = TeamIDs[packet.participants[19].teamId]
        teammate_car = 0

        player_id = packet.participants[19].driverId

        for i, racer in enumerate(packet.participants):
            if racer.teamId == team_id and racer.driverId != player_id:
                teammate_car = i
        result["teammate"] = teammate_car
        result["team_name"] = team_name

    teammate_results = None

    for field in packet_type._fields_:
        field_name = field[0]

        # maybe use this later to separate types?
        # field_type = field[1]

        if field_name == "header":
            continue

        value = getattr(packet, field_name)

        try:
            if isinstance(value, numbers.Number):
                result[field_name] = value
            # check if this is car or lap data, this means it's 22 elements long
            # on entry per car on the track.
            elif len(value) == 22:
                result = extract_all_car_array(value, players_car, result)
                if hasattr(packet, "participants"):
                    teammate_results = extract_all_car_array(
                        value, teammate_car, result
                    )
        except:
            pass
    return result, teammate_results


def extract_all_car_array(packet, players_car, result):

    data = packet[players_car]

    for field in data._fields_:
        name = field[0]
        value = getattr(data, name)

        if isinstance(value, numbers.Number):
            result[name] = value
        elif isinstance(value, ctypes.Array) and len(value) == 4:
            result[f"{name}_rl"] = value[0]
            result[f"{name}_rr"] = value[1]
            result[f"{name}_fl"] = value[2]
            result[f"{name}_fr"] = value[3]

    return result


def format_packet(packet):
    res = {}

    for (fname, ftype) in packet._fields_:

        value = getattr(packet, fname)
        if isinstance(value, PackedLittleEndianStructure):
            for k in value._fields_:
                res[k[0]] = getattr(value, k[0])
        elif isinstance(value, (int, float, bytes)):
            res[fname] = value
            pass
        elif isinstance(value, ctypes.Array):

            res[fname] = []
            for e in value:

                if isinstance(e, (int, float, bytes)):
                    try:
                        # decode odd string names
                        res[fname] = e.decode("utf-8", "strict")
                    except:
                        res[fname] = e
                else:
                    data = {}
                    for key in e._fields_:
                        reading = getattr(e, key[0])
                        if isinstance(reading, (int, float, bytes)):
                            try:
                                # decode drivers names
                                reading = reading.decode("utf-8", "strict")
                            except:
                                data[key[0]] = reading
                        else:
                            data[key[0]] = {}
                            data[key[0]][f"{key[0]}_rl"] = float(reading[0])
                            data[key[0]][f"{key[0]}_rr"] = float(reading[1])
                            data[key[0]][f"{key[0]}_fl"] = float(reading[2])
                            data[key[0]][f"{key[0]}_fr"] = float(reading[3])
                    res[fname].append(data)
        else:
            raise RuntimeError("Bad value {!r} of type {!r}".format(value, type(value)))
    return res
