import unittest
# from ckn.src.messagebroker.kafka_ingester import KafkaIngester
from ckn.src.data_generator.random_data_gen import RandomRequestGenerator
import time
from datetime import datetime, timedelta
from numpy.random import default_rng

from workload_generateor.baseline_generator import generate_baseline_load

REQUESTS_PER_SECOND = 1
TOTAL_RUN_TIME = 300
THOUSAND_RPS_TIMEOUT = 0.9
TENK_RPS_TIMEOUT = 1

class IngesterTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server_list = 'localhost:9092'
        topic = 'inference-requests8'
        # cls._producer = KafkaIngester(server_list, topic)
        cls._randgen = RandomRequestGenerator()

    @classmethod
    def test_request_steady_ingest(cls):
        total_run_time = 0.0
        current_time = datetime.now()
        for j in range(TOTAL_RUN_TIME):
            start_time = time.time()
            for i in range(REQUESTS_PER_SECOND):
                # request = cls._randgen.generate_request(service_prefix="es_2_service")
                random_generator = default_rng()

                # generates the requests per second and then sleeps for the duration of the second
                # this also writes to the output file
                current_time = current_time + timedelta(minutes=5)
                events, keys = generate_baseline_load(random_generator, current_time)
                time.sleep(THOUSAND_RPS_TIMEOUT)

                print('Step: {0} completed.'.format(j))

                # for k in range(len(keys)):
                #     cls._producer.send_request(events[j], key=keys[j])

            # time.sleep(TENK_RPS_TIMEOUT)
            # total_time = time.time() - start_time
            # total_run_time += total_time
            # print("done sending events... Total time: ", total_time)
        # print("avg time: ", total_run_time/10)
    #
    # @classmethod
    # def test_request_step_up_ingest(cls):
    #     rps = REQUESTS_PER_SECOND
    #     total_run_time = 0.0
    #     for j in range(TOTAL_RUN_TIME):
    #         start_time = time.time()
    #         for i in range(REQUESTS_PER_SECOND):
    #             request = cls._randgen.generate_request(service_prefix="es_2_service")
    #             cls._producer.send_request(request)
    #
    #         time.sleep(THOUSAND_RPS_TIMEOUT)
    #         total_time = time.time() - start_time
    #         total_run_time += total_time
    #         print("Sent {} events ... Total time:{} ".format(rps,total_time))
    #     print("avg time: ", total_run_time / 10)
    #
    # @classmethod
    # def test_request_spike_ingest(cls):
    #     total_run_time = 0.0
    #     for j in range(TOTAL_RUN_TIME):
    #         start_time = time.time()
    #         rps = REQUESTS_PER_SECOND
    #         if (j % 5 == 0):
    #             rps = REQUESTS_PER_SECOND * 3
    #         for i in range(rps):
    #             request = cls._randgen.generate_request(service_prefix="es_2_service")
    #             cls._producer.send_request(request)
    #
    #         time.sleep(THOUSAND_RPS_TIMEOUT)
    #         total_time = time.time() - start_time
    #         total_run_time += total_time
    #         print("Sent {} events ... Total time:{} ".format(rps, total_time))
    #     print("avg time: ", total_run_time / 10)


if __name__ == '__main__':
    unittest.main()