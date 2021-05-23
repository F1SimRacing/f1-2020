from typing import List

from influxdb import InfluxDBClient


class InfluxConnector:

    def __init__(self, database: str = 'telemetry',
                 host: str = 'localhost', port: int = 8086) -> None:

        self.connection = InfluxDBClient(host=host, port=port, database=database)

    def write_data(self, data: List):
        self.connection.write_points(data)
