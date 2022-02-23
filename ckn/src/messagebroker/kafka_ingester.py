from datetime import datetime
from json import dumps
from kafka import KafkaProducer
from util.util import get_request_json

class KafkaIngester:
    """
    Library class for ingesting information into CKN through Kafka.
    """

    def __init__(self, server_list, ckn_topic):
        self.producer = KafkaProducer(bootstrap_servers=[server_list],
                                      value_serializer=lambda x: dumps(x, default=str).encode('utf-8'))
        self.topic = ckn_topic

    def send_request(self, request):
        """
        Sends requests to CKN
        """
        self.producer.send(self.topic, request)
        pass
