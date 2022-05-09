import random


class RandomRequestGenerator:
    """
    Generates requests at random.
    """
    def generate_request(self, model_id=None, service_id=None, client_id=None):
        qos = round(random.uniform(0.5, 0.99), 15)
        qoa = round(random.uniform(0.5, 0.99), 15)
        qod = round(random.uniform(0.5, 0.99), 15)
        delay = round(random.uniform(0.5, 0.99), 15)
        delay_comm = round(random.uniform(0.5, 0.99), 15)
        delay_comp = round(random.uniform(0.5, 0.99), 15)
        if model_id is None:
            model_id = random.randint(0, 10)
        if service_id is None:
            service_id = random.randint(0, 5)
        if client_id is None:
            client_id = 'device_' + str(random.randint(0, 5))

        return self._get_json_req(qos, qoa, qod, delay, delay_comm, delay_comp, model_id, service_id, client_id)

    def _get_json_req(self, qos, qoa, qod, delay, delay_comm, delay_comp, model_id, service_id, client_id):
        request = {'QoS': qos, 'QoA': qoa, 'QoD': qod, 'delay': delay, 'delay_comm': delay_comm,
                   'delay_comp': delay_comp,
                   'model_id': model_id, 'service_id': service_id, 'client_id': client_id}
        return request
