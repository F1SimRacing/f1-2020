import ctypes
import numbers
import socket

from f1_2020_telemetry.packets import unpack_udp_packet, PackedLittleEndianStructure
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

MOTION_FIELDS = ['suspensionPosition', 'suspensionVelocity', 'suspensionAcceleration',
                 'wheelSpeed', 'wheelSlip', 'localVelocityX', 'localVelocityY',
                 'localVelocityZ',
                 'angularVelocityX', 'angularVelocityY', 'angularVelocityZ',
                 'angularAccelerationX',
                 'angularAccelerationY', 'angularAccelerationZ', 'frontWheelsAngle']

SESSION_FIELDS = [
    'weather', 'trackTemperature', 'airTemperature', 'totalLaps', 'trackLength',
    'sessionType', 'trackId', 'm_formula', 'sessionTimeLeft', 'sessionDuration',
    'pitSpeedLimit', 'gamePaused', 'isSpectating', 'spectatorCarIndex',
    'sliProNativeSupport', 'numMarshalZones', 'marshalZones', 'safetyCarStatus',
    'networkGame'
]


class Feed:

    def __init__(self, port: int = None):
        if not port:
            port = 20777

        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind(('', port))

    def get_latest(self):
        packet = unpack_udp_packet(self.socket.recv(2048))
        p = format_packet_v2(packet)

        # try:
        #     print(format_packet_v2(packet))
        # except Exception as exc:
        #     print('asdf')
        # motion data for moving a freaking platform!
        # if 'suspensionPosition' in p:
        #     p['motionData'] = {}
        #     for i in MOTION_FIELDS:
        #         p['motionData'][i] = p[i]
        #         del p[i]
        # if 'weather' in p:
        #     p['sessionData'] = {}
        #     for i in SESSION_FIELDS:
        #         p['sessionData'][i] = p[i]
        #         del p[i]
        #
        # if 'eventStringCode' in p:
        #     p['eventStringCode'] = p['eventStringCode'].decode("utf-8", "strict")
        return p


def format_packet_v2(packet, players_car=True):
    packet_type = type(packet)

    players_car = packet.header.playerCarIndex

    result = {
        'type': packet_type.__name__,
        'sessionTime': packet.header.sessionTime,
        'sessionUID': float(packet.header.sessionUID)
    }

    for field in packet_type._fields_:
        field_name = field[0]

        # maybe use this later to separate types?
        # field_type = field[1]

        if field_name == 'header':
            continue

        value = getattr(packet, field_name)

        try:
            if isinstance(value, numbers.Number):
                result[field_name] = value
            # check if this is car or lap data, this means it's 22 elements long
            # on entry per car on the track.
            elif len(value) == 22:
                result = extract_all_car_array(value, players_car, result)
        except:
            pass

 #
 #        sub_field = getattr(packet, top_level_field[0])
 #
 #        if isinstance(sub_field, numbers.Number):
 #            result[top_level_field[0]] = sub_field
 #            # print(f'{top_level_field[0]} {sub_field}')
 #        else:
 #            # fetch only the value from 22 array for the players number
 #
 #            # 0 – Rear Left(RL)
 #            # 1 – Rear
 #            # Right(RR)
 #            # 2 – Front
 #            # Left(FL)
 #            # 3 – Front
 #            # Right(FR)
 #            try:
 #                if isinstance(sub_field[players_car], numbers.Number):
 #                    try:
 #                        if len(sub_field) == 4:
 #                            result[top_level_field[0]] = {
 #                                'rl': sub_field[0],
 #                                'rr': sub_field[1],
 #                                'fl': sub_field[2],
 #                                'fr': sub_field[3]
 #                            }
 #                        else:
 #                            print('ffs')
 #                        continue
 #                    except Exception as exc:
 #                        print('damn!')
 #
 #                for players_car_data in type(sub_field[players_car])._fields_:
 #                    for attr_to_process in sub_field:
 #                        sub_sub_value = getattr(attr_to_process, players_car_data[0])
 #
 #                        if isinstance(sub_sub_value, numbers.Number):
 #                            result[players_car_data[0]] = sub_sub_value
 #
 #                        # deal with embedded types usually for tyres.
 #                        # for example CarStatusData_V1_Array_22
 #
 #                        elif len(getattr(attr_to_process, players_car_data[0])) == 4:
 #                            result[players_car_data[0]] = {
 #                                'rl': getattr(attr_to_process, players_car_data[0])[0],
 #                                'rr': getattr(attr_to_process, players_car_data[0])[1],
 #                                'fl': getattr(attr_to_process, players_car_data[0])[2],
 #                                'fr': getattr(attr_to_process, players_car_data[0])[3]
 #                            }
 #                        else:
 #                            logger.info(f'Missed {players_car_data}')
 #            except Exception as exc:
 #
 #                if hasattr(type(sub_field), '_fields_'):
 #                    for key in type(sub_field)._fields_:
 #                        print(getattr(sub_field, key[0]))
 #                        # result[getattr(sub_field, key[0])]
 #                else:
 #                    # most likely suspensions or similar with an array of 4
 # #                   print(f'{top_level_field[0]} -> {sub_field[0]}, {sub_field[1]},
 #                    #                   {sub_field[2]} ,{sub_field[3]}')
 #                    result[top_level_field[0]] = {
 #                                'rl': sub_field[0],
 #                                'rr': sub_field[1],
 #                                'fl': sub_field[2],
 #                                'fr': sub_field[3]
 #                            }
    return result


def extract_all_car_array(packet, players_car, result):

    data = packet[players_car]

    for field in data._fields_:
        name = field[0]
        value = getattr(data, name)

        if isinstance(value, numbers.Number):
            result[name] = value
        elif isinstance(value, ctypes.Array) and len(value) == 4:
            result[f'{name}_rl'] = value[0]
            result[f'{name}_rr'] = value[1]
            result[f'{name}_fl'] = value[2]
            result[f'{name}_fr'] = value[3]

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
                            data[key[0]][f'{key[0]}_rl'] = float(reading[0])
                            data[key[0]][f'{key[0]}_rr'] = float(reading[1])
                            data[key[0]][f'{key[0]}_fl'] = float(reading[2])
                            data[key[0]][f'{key[0]}_fr'] = float(reading[3])
                        # data[key[0]] = value
                    res[fname].append(data)
        else:
            raise RuntimeError(
                "Bad value {!r} of type {!r}".format(value, type(value)))
    return res
