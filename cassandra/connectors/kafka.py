from typing import Dict, List

from kafka import KafkaProducer

from cassandra.config import KafkaConfiguration


class KafkaConnector:
    """
    Send messages to Kafka.
    """

    def __init__(self, configuration: KafkaConfiguration):
        self.producer = KafkaProducer(bootstrap_servers=configuration.bootstrap_servers)

    def send(self, topic, message):
        self.producer.send(topic, message)

    def build_data(self, name: str, value, data: Dict) -> Dict:
        data[name] = value
        return data
