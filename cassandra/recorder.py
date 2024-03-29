import json
import logging
from typing import List, NamedTuple, Union

from f1_2020_telemetry.types import TrackIDs

from cassandra.config import RecorderConfiguration
from cassandra.connectors.heart_beat_monitor import SerialSensor, _detect_port
from cassandra.connectors.influxdb import InfluxDBConnector
from cassandra.connectors.kafka import KafkaConnector
from cassandra.telemetry.constants import PACKET_MAPPER, SESSION_TYPE
from cassandra.telemetry.source import Feed

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)


class Race(NamedTuple):
    circuit: str
    session_type: str
    session_uid: str


class DataRecorder:
    _kafka: Union[KafkaConnector, None] = None
    _kafka_unavailable: bool = False
    _influxdb: Union[InfluxDBConnector, None] = None

    def __init__(self, configuration: RecorderConfiguration, port: int = 20777) -> None:
        self.configuration: RecorderConfiguration = configuration
        self.feed = Feed(port=port)
        self.port = port

    @property
    def kafka(self):
        if not self._kafka and self.configuration.kafka and not self._kafka_unavailable:
            self._kafka = KafkaConnector(configuration=self.configuration.kafka)
            if not self._kafka.in_error:
                self._kafka_unavailable = True
        return self._kafka

    @property
    def influxdb(self):
        if not self._influxdb and self.configuration.influxdb:
            self._influxdb = InfluxDBConnector(
                configuration=self.configuration.influxdb
            )

        return self._influxdb

    def write_to_influxdb(self, data: List) -> bool:
        if not self.influxdb:
            return False

        self.influxdb.write(data)
        return True

    def get_heart_rate(self):
        sensor_reader = SerialSensor(port=_detect_port())
        return sensor_reader.read()

    def listen(self):
        race_details = None
        logger.info(f'Starting server to receive telemetry data on port: {self.port}.')
        packet_name: str = 'unknown'
        lap_number = 1

        while True:
            packet, teammate = self.feed.get_latest()

            if not packet:
                continue

            influxdb_data = []
            kafka_data = {}

            if packet['type'] == 'PacketSessionData_V1' and not race_details:
                race_details = Race(
                    circuit=TrackIDs[packet['trackId']],
                    session_type=SESSION_TYPE[packet['sessionType']],
                    session_uid=packet['sessionUID'],
                )

            # we are late, so spin until we find out which race we are at
            if not race_details:
                continue

            if packet['type'] == 'PacketLapData_V1':
                lap_number = int(packet['currentLapNum'])

            if packet['type'] in PACKET_MAPPER.keys():
                packet_name: str = 'unknown'

                for name, value in packet.items():

                    if name == 'name':
                        packet_name = value

                    if name in ['type', 'mfdPanelIndex', 'buttonStatus', 'name']:
                        continue

                    # drivers name are bytes
                    if name == 'name' and packet['type'] == 'PacketParticipantsData_V1':
                        if type(value) == bytes:
                            value = value.decode('utf-8')

                    # FIXME
                    if name not in ['sessionUID', 'team_name']:
                        if self.influxdb:
                            influxdb_data.append(
                                f'{packet_name},track={race_details.circuit},'
                                f'lap={lap_number},'
                                f'session_uid={race_details.session_uid},'
                                f'session_type={race_details.session_type}'
                                f' {name}={value}'
                            )

                        if self.kafka:
                            kafka_data = self.kafka.build_data(
                                name=name, value=value, data=kafka_data
                            )

            if self.kafka:
                kafka_msg = {
                    'lap_number': lap_number,
                    'circuit': race_details.circuit,
                    'session_uid': race_details.session_uid,
                    'session_type': race_details.session_type,
                    'data': kafka_data,
                }
                if packet_name:
                    self.kafka.send(packet_name, json.dumps(kafka_msg).encode('utf-8'))

            if self.influxdb:
                self.influxdb.write(influxdb_data)
