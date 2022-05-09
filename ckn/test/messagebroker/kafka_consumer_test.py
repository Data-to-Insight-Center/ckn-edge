import unittest
from ckn.src.messagebroker.kafka_consumer import KafkaCKNConsumer


class IngesterTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server_list = ['172.27.29.200:9092']
        topic = 'inference-requests'
        cls._consumer = KafkaCKNConsumer(server_list, topic)

    @classmethod
    def test_request_ingest(cls):
        cls._consumer.consume()

if __name__ == '__main__':
    unittest.main()