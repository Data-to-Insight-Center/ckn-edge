from ingest.parser import parse_file
from util.graph_scripter import create_graph_request, create_all_requests
from ingest.dbConnect import Database
import numpy as np
from messagebroker.kafka_ingester import KafkaIngester
from util.util import get_request_json

def main():
    # FILE = "/mnt/d/git/ckn-edge/ckn/test/ingest/resources/qos_pred_sample.csv"
    FILE = "D:/git/ckn-edge/ckn/test/ingest/resources/qos_pred_raspi-2-es3.csv"
    DB_USER = "neo4j"
    DB_URI = "bolt://192.168.86.178:11003"
    DB_PWD = "root"
    KAFKA_TOPIC = "inf-events"
    server_list = 'localhost:9092'

    db = Database(DB_URI, DB_USER, DB_PWD)
    broker = KafkaIngester(server_list, KAFKA_TOPIC)

    values, keys = parse_file(FILE)
    requests = []
    for i in range(6):
        model_id = "es_2_service_0_model_" + str(i)
        client_id = "jetson-1"
        model_based_req = values[np.where(values[:, 8] == i)]
        requests += create_all_requests(model_based_req, model_id, client_id)

    print("sending {} requests ...".format(len(requests)))
    # for kafka
    # temp_request = get_request_json(values[0])
    # print(temp_request)

    # sending requests to Kafka
    # broker.send_request(temp_request)

    # db.print_greeting("Hello World")
    for request in requests:
        db.run_cypher_query(request)
    db.close()

if __name__ == "__main__":
    main()