from ckn.src.util.constants import INGEST_REQUEST_TO_GRAPH, INGEST_PROCESSED_REQUEST_TO_GRAPH, INGEST_AGGR_REQUEST_TO_GRAPH


def create_graph_request(req_values, model_name, client_id):
    qos = req_values[2]
    qoa = req_values[3]
    qod = req_values[4]
    delay = req_values[5]
    delay_comm = req_values[6]
    delay_comp = req_values[7]
    model_id = req_values[8]
    service_id = req_values[9]
    # client_id = req_values[-1]
    req_id = 223

    request = INGEST_REQUEST_TO_GRAPH.format(model_name, client_id, qos, qoa, qod, delay, delay_comm, delay_comp, model_id, service_id, req_id)
    return request


def create_all_requests(values, model_id, client_id):
    result = []
    for i in range(values.shape[0]):
        result.append(create_graph_request(values[i], model_id, client_id))
    return result


def create_graph_request_aggregated_json(request, request_id):
    """
    Generates the graph request cypher query from a given JSON request from the consumer for the aggregated events
    Args:
        request:
        graph_node_id:
        request_id:

    Returns:
    generated cypher insert query.
    """
    avg_accuracy = request['average_accuracy']
    avg_delay = request['average_delay']
    service_id = request['service_id']
    client_id = request['client_id']
    server_id = request['server_id']
    window_time = request['timestamp']

    graph_request = INGEST_AGGR_REQUEST_TO_GRAPH.format(server_id, client_id, avg_accuracy, avg_delay,
                                                        service_id, window_time)
    return graph_request


def create_graph_request_from_json(request, request_id):
    """
    Generates the graph request cypher query from a given JSON request from the consumer
    Args:
        request:
        graph_node_id:
        request_id:

    Returns:
    generated cypher insert query.
    """
    accuracy = request['accuracy']
    delay = request['delay']
    service_id = request['service_id']
    client_id = request['client_id']

    graph_request = INGEST_REQUEST_TO_GRAPH.format(service_id, client_id, accuracy, delay, service_id, request_id)
    return graph_request


def create_graph_request_from_processed_json(request, request_id):
    """
    Generates the graph request cypher query from a given JSON request from the processed dataset (with QoA QoD)
    Args:
        request:
        graph_node_id:
        request_id:

    Returns:
    generated cypher insert query.
    """
    qos = request['QoS']
    qoa = request['QoA']
    qod = request['QoD']
    delay = request['delay']
    delay_comm = request['delay_comm']
    delay_comp = request['delay_comp']
    model_id = request['model_id']
    service_id = request['service_id']
    client_id = request['client_id']

    graph_request = INGEST_PROCESSED_REQUEST_TO_GRAPH.format(service_id, client_id, qos, qoa, qod, delay, delay_comm, delay_comp,
                                             model_id, service_id, request_id)
    return graph_request
