"""
Connector for sending data to the time series database InfluxDB.

See - https://www.influxdata.com/
"""
from pathlib import Path
from typing import List

from influxdb_client.client.write_api import SYNCHRONOUS

from cassandra.config import load_config
from influxdb_client import InfluxDBClient
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

HOME: str = Path.home()
CONFIG_FILE_NAME: str = 'config.ini'


class InfluxDBConnector:

    def __init__(self, config_filename: str) -> None:

        self.config_file_name: str = config_filename
        self._connection = None
        self._write_api = None
        self.config = load_config()['influxdb']

    @property
    def connection(self) -> InfluxDBClient:
        if not self._connection:
            self._connection = InfluxDBClient(url=self.config['host'],
                                              token=self.config['token'])
        return self._connection

    @property
    def write_api(self):
        if not self._write_api:
            self._write_api = self.connection.write_api(write_options=SYNCHRONOUS)
        return self._write_api

    def write(self, data: List[str]):
        """
        data = [
            "mem,host=host1 used_percent=23.43234543",
            "mem,host=host1 available_percent=15.856523"
            ]
        A list of strings, the format for the data is:
        name,tag_name=tag_value field=values

        name - the high level name, in the above case memory
        tag_name - the list of tags
        field - name of the field and the value

        Example:
            "car_status,circuit=monza,lap=3,race_type=championship speed=287"
        """

        # explore:
        # write_api = client.write_api(write_options=ASYNCHRONOUS)
        #
        # _point1 = Point("my_measurement").tag("location", "Prague").field("temperature",
        #                                                                   25.3)
        # _point2 = Point("my_measurement").tag("location", "New York").field(
        #     "temperature", 24.3)
        #
        # async_result = write_api.write(bucket="my-bucket", record=[_point1, _point2])
        # async_result.get()
        #
        # client.close()
        # or
        # with _client.write_api(write_options=WriteOptions(batch_size=500,
        #                                                       flush_interval=10_000,
        #                                                       jitter_interval=2_000,
        #                                                       retry_interval=5_000,
        #                                                       max_retries=5,
        #                                                       max_retry_delay=30_000,
        #                                                       exponential_base=2))
        #                                                       as _write_client:
        # see https://github.com/influxdata/influxdb-client-python

        # write_api = self.connection.write_api(write_options=SYNCHRONOUS)
        self.write_api.write(self.config['bucket'], self.config['org'],
                                            data)
        # async_result.get()
