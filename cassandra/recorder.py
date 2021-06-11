from typing import NamedTuple
from f1_2020_telemetry.types import TrackIDs

from cassandra.connectors.influxdb import InfluxDBConnector
from cassandra.telemetry.constants import PACKET_MAPPER, SESSION_TYPE, TYRE_COMPOUND
from cassandra.telemetry.source import Feed
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


class Race(NamedTuple):
    circuit: str
    session_type: str
    session_uid: str


def main():
    race_details = None

    influx_conn = InfluxDBConnector('/Users/channam/.config/cassandra/config.ini')
    logger.info("Starting server to receive telemetry data.")
    feed = Feed()
    lap_number = 1

    while True:
        packet = feed.get_latest()

        if not packet:
            continue

        data = []
        if packet["type"] == "PacketSessionData_V1" and not race_details:
            # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P
            # 5 = Q1, 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ
            # 10 = R, 11 = R2, 12 = Time Trial
            race_details = Race(
                circuit=TrackIDs[packet["trackId"]],
                session_type=SESSION_TYPE[packet["sessionType"]],
                session_uid=packet["sessionUID"]
            )

        # we are late, so spin until we find out which race we are at
        if not race_details:
            continue

        if packet["type"] == "PacketLapData_V1":
            lap_number = packet["currentLapNum"]

        if packet["type"] in PACKET_MAPPER.keys():
            packet_name: str = 'unknown'
            for name, value in packet.items():

                if name == 'name':
                    packet_name = value

                if name in ["type", "mfdPanelIndex", "buttonStatus", 'name']:
                    continue

                # drivers name are bytes
                if name == "name" and packet["type"] == "PacketParticipantsData_V1":
                    if type(value) == bytes:
                        value = value.decode("utf-8")

                data.append(
                    f'{packet_name},track={race_details.circuit},'
                    f'lap={lap_number},session_uid={race_details.session_uid},'
                    f'session_type={race_details.session_type}'
                    f' {name}={value}'
                    # {
                    #     "measurement": name,
                    #     "tags": {
                    #         "type": packet["name"],
                    #         "track": race_details.circuit,
                    #         "lap": lap_number,
                    #         "total_laps": race_details.total_laps,
                    #     },
                    #     "fields": {"value": value},
                    # }
                )
                # data = ["mem,host=host1 used_percent=23.43234543",
                #             "mem,host=host1 available_percent=15.856523"]
            a = 1
            # influx_conn.write(data)
            #influx_conn.write(data)


if __name__ == "__main__":
    main()
