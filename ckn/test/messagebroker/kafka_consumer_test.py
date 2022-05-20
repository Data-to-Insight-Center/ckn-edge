import unittest
from ckn.src.messagebroker.kafka_consumer import KafkaCKNConsumer


class IngesterTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server_list = ['localhost:9092']
        topic = 'inference-requests'
        db_user = "neo4j"
        db_uri = "bolt://172.28.96.1:11003"
        db_pwd = "root"
        cls._consumer = KafkaCKNConsumer(server_list, topic, db_uri, db_user, db_pwd)

    @classmethod
    def test_request_ingest(cls):
        cls._consumer.consume()

if __name__ == '__main__':
    unittest.main()