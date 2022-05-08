import unittest
from ckn.src.messagebroker.kafka_ingester import KafkaIngester


class IngesterTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server_list = 'localhost:9092'
        topic = 'inference-events'
        cls._producer = KafkaIngester(server_list, topic)

    @classmethod
    def test_request_ingest(cls):
        test = {'name': 20}
        cls._producer.send_request(test)

if __name__ == '__main__':
    unittest.main()