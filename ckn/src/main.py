from ingest.parser import parse_file
from util.graph_scripter import create_graph_request, create_all_requests
from ingest.dbConnect import Database
import numpy as np

def main():
    # FILE = "/mnt/d/git/ckn-edge/ckn/test/ingest/resources/qos_pred_sample.csv"
    FILE = "D:/git/ckn-edge/ckn/test/ingest/resources/qos_pred_sample.csv"
    DB_USER = "neo4j"
    DB_URI = "bolt://127.0.0.1:11003"
    DB_PWD = "root"

    db = Database(DB_URI, DB_USER, DB_PWD)
    values, keys = parse_file(FILE)
    requests = []
    for i in range(6):
        model_id = "es_1_service_0_model_" + str(i)
        model_based_req = values[np.where(values[:, 8] == i)]
        requests += create_all_requests(model_based_req, model_id)

    print(len(requests))
    # print(requests[0])
    db.print_greeting("Hello World")
    # for request in requests:
    #     db.run_cypher_query(request)
    db.close()

if __name__ == "__main__":
    main()