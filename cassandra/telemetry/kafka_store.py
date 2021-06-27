import json

from cassandra.telemetry.source import Feed
from cassandra.data_storage.kafka_connector import KafkaConnector


def main():
    feed = Feed()
    kafka_connector = KafkaConnector("jarvis")

    while True:
        data = feed.get_latest()
        try:
            msg = json.dumps(data)
            if "lapData" in data:
                kafka_connector.send("lap_data", str.encode(msg))
            elif "carTelemetryData" in data:
                kafka_connector.send("car_telemetry_data", str.encode(msg))
            elif "carMotionData" in data:
                kafka_connector.send("car_motion_data", str.encode(msg))
            elif "motionData" in data:
                kafka_connector.send("motion_data", str.encode(msg))
            elif "buttonStatus" in data:
                kafka_connector.send("button_status_data", str.encode(msg))
            elif "sessionData" in data:
                kafka_connector.send("session_data", str.encode(msg))
        except Exception as exc:
            print(f"DAMN! {data}")


if __name__ == "__main__":
    main()
