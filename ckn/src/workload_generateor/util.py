import time


def generate_request(device, server, service, accuracy, delay, now_datetime):
    # now_time_millis = round(time.time() * 1000)
    return {"accuracy": accuracy, "delay": delay, "server_id": server, "service_id": service, "client_id": device, "added_time": now_datetime}
    # return {"accuracy": accuracy, "delay": delay, "server_id": server, "service_id": service, "client_id": device}


def generate_stream_event_key(client_id, service_id, edge_server):
    return str(client_id + "-" +edge_server + "-" + service_id)