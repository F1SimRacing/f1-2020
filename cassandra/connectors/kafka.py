from kafka import KafkaProducer


class KafkaConnector:
    """
    Send messages to Kafka.
    """

    def __init__(self, host: str = None):

        if not host:
            host = 'localhost'
        self.producer = KafkaProducer(bootstrap_servers=f'{host}:9092')

    def send(self, topic, message):
        self.producer.send(topic, message)
