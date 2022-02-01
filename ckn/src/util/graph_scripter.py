from util.constants import INGEST_REQUEST_TO_GRAPH


def create_graph_request(req_values, model_name):
    qos = req_values[2]
    qoa = req_values[3]
    qod = req_values[4]
    delay = req_values[5]
    delay_comm = req_values[6]
    delay_comp = req_values[7]
    model_id = req_values[8]
    service_id = req_values[9]
    client_id = req_values[-1]
    req_id = 223

    request = INGEST_REQUEST_TO_GRAPH.format(model_name, client_id, qos, qoa, qod, delay, delay_comm, delay_comp, model_id, service_id, req_id)
    return request


def create_all_requests(values, model_id):
    result = []
    for i in range(values.shape[0]):
        result.append(create_graph_request(values[i], model_id))
    return result
