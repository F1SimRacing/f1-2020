from cassandra.data_storage.influx import InfluxConnector
from cassandra.telemetry.source import Feed
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)


def main():

    influx_conn = InfluxConnector()

    logger.info('Starting server to receive telemetry data.')
    feed = Feed()
    while True:
        packet = feed.get_latest()
        if packet['type'] == 'PacketCarTelemetryData_V1':
            # data = []
            # print(packet)
            # for name, value in packet.items():
            #     data.append(
            #         {
            #             "measurement": name,
            #             "tags": {
            #                 "type": "car_telemetry"
            #             },
            #             "time": packet['sessionTime'],
            #             "fields": {
            #                 "value": 0.64
            #             }
            #         }
            #     )

            data = []
            print(f'engineRPM -> {packet["engineRPM"]}')
            data.append(
                {
                    "measurement": "engineRPM",
                    "tags": {
                        "type": "car_telemetry"
                    },
                    # "time": packet['sessionTime'],
                    "fields": {
                        "value": packet['engineRPM']
                    }
                }
            )
            influx_conn.write_data(data)


if __name__ == '__main__':
    main()
