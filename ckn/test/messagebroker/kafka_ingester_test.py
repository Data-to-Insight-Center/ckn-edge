import unittest
from ckn.src.messagebroker.kafka_ingester import KafkaIngester
from ckn.src.data_generator.random_data_gen import RandomRequestGenerator


class IngesterTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server_list = 'localhost:9092'
        topic = 'inference-requests'
        cls._producer = KafkaIngester(server_list, topic)
        cls._randgen = RandomRequestGenerator()

    @classmethod
    def test_request_ingest(cls):
        for i in range(3):
            request = cls._randgen.generate_request(service_prefix="es_2_service")
            cls._producer.send_request(request)
            print(request)
        print("done sending events...")


if __name__ == '__main__':
    unittest.main()