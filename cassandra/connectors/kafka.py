from typing import Dict

from kafka import KafkaProducer


class KafkaConnector:
    """
    Send messages to Kafka.
    """

    def __init__(self, host: str = None):

        if not host:
            host = "localhost:9092"
        self.producer = KafkaProducer(bootstrap_servers=host)

    def send(self, topic, message):
        self.producer.send(topic, message)

    def build_data(self, name: str, value, data: Dict) -> Dict:
        data[name] = value
        return data
