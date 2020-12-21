from cassandra.data_storage.influx import InfluxConnector
from cassandra.telemetry.source import Feed
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)


def main():

    influx_conn = InfluxConnector(host='192.168.0.100')
    logger.info('Starting server to receive telemetry data.')
    feed = Feed()
    lap_number = 1

    while True:
        packet = feed.get_latest()

        data = []
        if packet['type'] == 'PacketLapData_V1':
            lap_number = packet['currentLapNum']

        if packet['type'] in ['PacketCarTelemetryData_V1', 'PacketLapData_V1',
                              'PacketMotionData_V1', 'PacketSessionData_V1',
                              'PacketCarStatusData_V1']:

            for name, value in packet.items():
                if name in ['type', 'mfdPanelIndex',
                            'buttonStatus']:
                    continue

                data.append(
                    {
                        "measurement": name,
                        "tags": {
                            "type": "car_telemetry",
                            "track": "monza",

                        },
                        "fields": {
                            "value": value,
                            "lap": lap_number

                        }
                    }
                    )
            influx_conn.write_data(data)


if __name__ == '__main__':
    main()
