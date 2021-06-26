import json
from typing import NamedTuple
from f1_2020_telemetry.types import TrackIDs

from cassandra.connectors.influxdb import InfluxDBConnector
from cassandra.telemetry.constants import PACKET_MAPPER, SESSION_TYPE
from cassandra.telemetry.heart_beat_monitor import SerialSensor, _detect_port
from cassandra.connectors.kafka import KafkaConnector
from cassandra.telemetry.source import Feed
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

SEND_TO_KAFKA = False
SEND_TO_INFLUXDB = False


class Race(NamedTuple):
    circuit: str
    session_type: str
    session_uid: str


def main():
    race_details = None

    if SEND_TO_INFLUXDB:
        influx_conn = InfluxDBConnector('/Users/channam/.config/cassandra/config.ini')

    if SEND_TO_KAFKA:
        kafka_conn = KafkaConnector('ultron:9092')
    logger.info("Starting server to receive telemetry data.")
    feed = Feed(port=20788)
    lap_number = 1

    while True:
        packet, teammate = feed.get_latest()

        # sensor_reader = SerialSensor(port=_detect_port())
        # reading = sensor_reader.read()

        if not packet:
            continue

        data = []
        if packet["type"] == "PacketSessionData_V1" and not race_details:
            race_details = Race(
                circuit=TrackIDs[packet["trackId"]],
                session_type=SESSION_TYPE[packet["sessionType"]],
                session_uid=packet["sessionUID"]
            )

        # we are late, so spin until we find out which race we are at
        if not race_details:
            continue

        if packet["type"] == "PacketLapData_V1":
            lap_number = int(packet["currentLapNum"])

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

                # FIXME
                if name not in ['sessionUID', 'team_name']:
                    data.append(
                        f'{packet_name},track={race_details.circuit},'
                        f'lap={lap_number},session_uid={race_details.session_uid},'
                        f'session_type={race_details.session_type}'
                        f' {name}={value}'
                    )

                    if SEND_TO_KAFKA:
                        msg = {
                            'lap_number': lap_number,
                            'circuit': race_details.circuit,
                            'session_uid': race_details.session_uid,
                            'session_type': race_details.session_type,
                            name: value

                        }
                        kafka_conn.send(packet_name, json.dumps(msg).encode('utf-8'))

                    # if reading:
                    #     print(f'{reading}')
                    #     data.append(
                    #         # f"health,tag=pulse pulse={reading['bpm']}"
                    #         f'health,track={race_details.circuit},'
                    #         f'lap={lap_number},session_uid={race_details.session_uid},'
                    #         f'session_type={race_details.session_type},'
                    #         f"stat=pulse pulse={reading['bpm']}"
                    #     )
                    # influx_conn.write(data)

            influx_conn.write(data)


if __name__ == "__main__":
    main()
