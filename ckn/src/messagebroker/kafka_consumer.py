from datetime import datetime
from json import loads
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import threading
from ckn.src.util.graph_scripter import create_graph_request_from_json


class KafkaCKNConsumer():

    def __init__(self, server_list, ckn_topic, poll_timeout=1.0, group_id='group-ckn'):
        self.topic = ckn_topic
        self.server_list = server_list
        self.group_id = group_id
        self.timeout = poll_timeout
        self.running = True

        # # using it as a thread
        # threading.Thread.__init__(self)
        # self.stop = threading.Event()

        self.consumer = KafkaConsumer(
            # self.topic,
            bootstrap_servers=self.server_list,
            enable_auto_commit=True,
            group_id=self.group_id,
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )

    def consume(self):
        try:
            self.consumer.subscribe(self.topic)
            print("subscribing to topic ...")
            for message in self.consumer:
                if message is None:
                    print("Message is none")
                    continue
                #
                # elif message.error():
                #     print(message.error())

                else:
                    self.process_message(message.value)
        finally:
            self.consumer.close()

    def process_message(self, message):
        request = create_graph_request_from_json(message, "temp_node_id", 222)
        print(request)

    def shutdown(self):
        self.running = False