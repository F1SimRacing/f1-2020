from typing import NamedTuple

from f1_2020_telemetry.packets import TrackIDs

from cassandra.data_storage.influx import InfluxConnector
from cassandra.telemetry.constants import PACKET_MAPPER
from cassandra.telemetry.source import Feed
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

"""
Lap is part of a Session which is part of a Race Weekend.
"""


class Race(NamedTuple):
    circuit: str
    total_laps: int


def main():
    race_details = None

    influx_conn = InfluxConnector(host='192.168.0.100')
    logger.info('Starting server to receive telemetry data.')
    feed = Feed()
    lap_number = 1

    while True:
        packet = feed.get_latest()

        data = []
        if packet['type'] == 'PacketLapData_V1':
            lap_number = packet['currentLapNum']

        if packet['type'] == 'PacketSessionData_V1' and not race_details:
            race_details = Race(
                circuit=TrackIDs[packet['trackId']],
                total_laps=packet['totalLaps']
            )

        if packet['type'] in PACKET_MAPPER.keys():
            for name, value in packet.items():
                if name in ['type', 'mfdPanelIndex',
                            'buttonStatus']:
                    continue

                # drivers name are bytes
                if name == 'name':
                    value = value.decode('utf-8')

                data.append(
                    {
                        "measurement": name,
                        "tags": {
                            "type": packet['name'],
                            "track": race_details.circuit,
                        },
                        "fields": {
                            "value": value,
                            "lap": lap_number,
                            'total_laps': race_details.total_laps
                        }
                    }
                )
                influx_conn.write_data(data)


if __name__ == '__main__':
    main()
