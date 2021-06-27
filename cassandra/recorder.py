import json
from typing import NamedTuple, List
from f1_2020_telemetry.types import TrackIDs

from cassandra.config import RecorderConfiguration, load_config
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


class DataRecorder:

    def __init__(self, config: RecorderConfiguration, port: int = 20777) -> None:
        self.configuration: RecorderConfiguration = config
        self.feed = Feed(port=port)

        if self.configuration.kafka:
            self.kafka: KafkaConnector = KafkaConnector('ultron:9092')
        else:
            self.kafka = None

        if self.configuration.influxdb:
            self.influxdb: InfluxDBConnector = InfluxDBConnector(
                self.configuration.influxdb)
        else:
            self.influxdb = None

    def write_to_influxdb(self, data: List) -> bool:
        if not self.influxdb:
            return False
        self.influxdb.write(data)

    def get_heart_rate(self):
        sensor_reader = SerialSensor(port=_detect_port())
        reading = sensor_reader.read()

    def listen(self):
        race_details = None
        logger.info("Starting server to receive telemetry data.")

        lap_number = 1

        while True:
            packet, teammate = self.feed.get_latest()

            if not packet:
                continue

            influxdb_data = []
            kafka_data = {}

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
                        if self.influxdb:
                            influxdb_data.append(
                                f'{packet_name},track={race_details.circuit},'
                                f'lap={lap_number},session_uid={race_details.session_uid},'
                                f'session_type={race_details.session_type}'
                                f' {name}={value}'
                            )

                        if self.kafka:
                            kafka_data = self.kafka.build_data(
                                name=name,
                                value=value,
                                data=kafka_data
                            )

            if self.kafka:
                kafka_msg = {
                    'lap_number': lap_number,
                    'circuit': race_details.circuit,
                    'session_uid': race_details.session_uid,
                    'session_type': race_details.session_type,
                    'data': kafka_data
                }
                self.kafka.send(
                    packet_name,
                    json.dumps(kafka_msg).encode('utf-8')
                )

            if self.influxdb:
                self.influxdb.write(influxdb_data)


if __name__ == "__main__":
    config = load_config()
    recorder = DataRecorder(config, port=20788)

    recorder.listen()
