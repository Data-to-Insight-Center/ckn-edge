import unittest
from ckn.src.messagebroker.kafka_consumer import KafkaCKNConsumer
from jproperties import Properties


class IngesterTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # configs = Properties()
        # with open('example.properties', 'rb') as read_prop:
        #     configs.load(read_prop)

        server_list = ['localhost:9092']
        topic = 'aggregated-events'
        db_user = "neo4j"
        db_uri = "bolt://localhost:7687"
        db_pwd = "root"
        consumer_threadpool_size = 10
        max_poll_records = 500
        cls._consumer = KafkaCKNConsumer(server_list, topic, db_uri, db_user, db_pwd, consumer_threadpool_size, max_poll_records)

    @classmethod
    def test_request_ingest(cls):
        cls._consumer.consume()

if __name__ == '__main__':
    unittest.main()