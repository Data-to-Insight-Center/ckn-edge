import datetime
import random


class RandomRequestGenerator:
    """
    Generates processed requests at random.
    """
    def generate_processed_request(self, service_prefix=None, model_prefix=None, client_id=None):
        qos = round(random.uniform(0.5, 0.99), 15)
        qoa = round(random.uniform(0.5, 0.99), 15)
        qod = round(random.uniform(0.5, 0.99), 15)
        delay = round(random.uniform(0.5, 0.99), 15)
        delay_comm = round(random.uniform(0.5, 0.99), 15)
        delay_comp = round(random.uniform(0.5, 0.99), 15)
        # todo: change this to accommodate proper data once the format is known
        if model_prefix is None:
            model_id = random.randint(0, 10)
        else:
            model_id = model_prefix + "_" + str(random.randint(0, 3))
        if service_prefix is None:
            service_id = random.randint(0, 5)
        else:
            service_id = service_prefix + "_0"
        if client_id is None:
            client_id = 'raspi-' + str(random.randint(1, 3))

        return self._get_json_processed_req(qos, qoa, qod, delay, delay_comm, delay_comp, model_id, service_id, client_id)

    """
    Generates requests at random.
    """
    def generate_request(self, service_prefix=None, client_id=None, added_time=None):
        #todo: make this added time to ingest custom time
        accuracy = round(random.uniform(0.5, 0.99), 15)
        delay = round(random.uniform(0.1, 10), 15)
        # todo: change this to accommodate proper data once the format is known
        if service_prefix is None:
            service_id = random.randint(0, 5)
        else:
            service_id = service_prefix + "_0"
        if client_id is None:
            client_id = 'raspi-' + str(random.randint(1, 3))

        return self._get_json_req(accuracy, delay, service_id, client_id, added_time)

    def _get_json_req(self, accuracy, delay, service_id, client_id, added_time):
        return {'accuracy': accuracy, 'delay': delay, 'service_id': service_id, 'client_id': client_id, 'added_time': added_time}

    def _get_json_processed_req(self, qos, qoa, qod, delay, delay_comm, delay_comp, model_id, service_id, client_id):
        request = {'QoS': qos, 'QoA': qoa, 'QoD': qod, 'delay': delay, 'delay_comm': delay_comm,
                   'delay_comp': delay_comp,
                   'model_id': model_id, 'service_id': service_id, 'client_id': client_id}
        return request
