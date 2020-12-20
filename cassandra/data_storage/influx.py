from typing import List

from influxdb import InfluxDBClient


class InfluxConnector:

    def __init__(self, database: str = 'telemetry',
                 host: str = None, port: str = None) -> None:
        if not port:
            port = 8086
        if not host:
            host = 'localhost'

        self.connection = InfluxDBClient(host=host, port=port, database=database)

    def write_data(self, data: List):
        self.connection.write_points(data)
