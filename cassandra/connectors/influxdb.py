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
        self.config = load_config()['influxdb']

    @property
    def connection(self) -> InfluxDBClient:
        if not self._connection:
            self._connection = InfluxDBClient(url=self.config['host'],
                                              token=self.config['token'])
        return self._connection

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
        write_api = self.connection.write_api(write_options=SYNCHRONOUS)
        write_api.write(self.config['bucket'], self.config['org'], data)
