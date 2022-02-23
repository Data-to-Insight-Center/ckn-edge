def get_request_json(req_values):
    qos = req_values[2]
    qoa = req_values[3]
    qod = req_values[4]
    delay = req_values[5]
    delay_comm = req_values[6]
    delay_comp = req_values[7]
    model_id = req_values[8]
    service_id = req_values[9]
    client_id = req_values[10]

    request = {'QoS': qos, 'QoA': qoa, 'QoD': qod, 'delay': delay, 'delay_comm': delay_comm, 'delay_comp': delay_comp,
               'model_id': model_id, 'service_id': service_id, 'client_id': client_id}
    return request
