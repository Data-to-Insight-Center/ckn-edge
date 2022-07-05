import time


def generate_request(device, server, service, accuracy, delay, now_time_millis):
    # now_time_millis = round(time.time() * 1000)
    return {'accuracy': accuracy, 'delay': delay, 'server': server, 'service': service, 'client_id': device, 'added_time': now_time_millis}
