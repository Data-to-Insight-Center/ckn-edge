from datetime import datetime
from json import dumps
from kafka import KafkaProducer


class DataIngester:
    """
    Library class for ingesting information into CKN from the Codar system.
    """

    def __init__(self, server_list, ckn_topic):
        self.producer = KafkaProducer(bootstrap_servers=[server_list],
                                      value_serializer=lambda x: dumps(x, default=str).encode('utf-8'))
        self.topic = ckn_topic

    def init_campaign(self, campaign_id, properties=None):
        """
        Initializes a campaign.
        """
        campaign_data = {'type': 'campaign', 'created_time': datetime.now(), 'id': campaign_id, 'status': "CREATED"}
        if properties:
            campaign_data.update(properties)
        self.producer.send(self.topic, campaign_data)
        pass

    def init_group(self, campaign_id, group_id, properties=None):
        """
        Initializes a group inside a campaign.
        """
        group_data = {'type': 'group', 'created_time': datetime.now(), 'id': group_id, 'campaign_id': campaign_id, 'status': "CREATED"}
        if properties:
            group_data.update(properties)
        self.producer.send(self.topic, group_data)

    def init_run(self, group_id, run_id, properties=None):
        """
        Initializes a run inside a group.
        """
        run_data = {'type': 'run', 'created_time': datetime.now(), 'id': run_id, 'group_id': group_id, 'status': "CREATED"}
        if properties:
            run_data.update(properties)
        self.producer.send(self.topic, run_data)

    def init_task(self, run_id, task_id, properties=None):
        """
        Initializes a task inside a run.
        """
        task_data = {'type': 'task', 'created_time': datetime.now(), 'id': task_id, 'run_id': run_id,
                      'status': "CREATED"}
        if properties:
            task_data.update(properties)
        self.producer.send(self.topic, task_data)

    def init_input(self, task_id, input_id, properties=None):
        """
        Initializes a input for a task.
        """
        task_data = {'type': 'input', 'created_time': datetime.now(), 'id': input_id, 'task_id': task_id,
                      'status': "CREATED"}
        if properties:
            task_data.update(properties)
        self.producer.send(self.topic, task_data)

    def add_properties(self, id, properties):
        """
        Adds properties to any entitiy with an id
        """
        data = {'type': 'properties', 'id': id}
        data.update(properties)
        self.producer.send(self.topic, data)