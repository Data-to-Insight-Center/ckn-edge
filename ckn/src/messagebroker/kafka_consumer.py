from datetime import datetime
from json import loads
from kafka import KafkaConsumer
from kafka.errors import KafkaError


class KafkaCKNConsumer:

    def __init__(self, server_list, ckn_topic, poll_timeout=1.0, group_id='group-ckn'):
        self.topic = ckn_topic
        self.server_list = server_list
        self.group_id = group_id
        self.timeout = poll_timeout
        self.running = True

        self.consumer = KafkaConsumer(
            # self.topic,
            bootstrap_servers=self.server_list,
            enable_auto_commit=True,
            group_id=self.group_id,
            # value_deserializer=lambda x: loads(x.decode('utf-8'))
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
                    print('processing message')
                    self.process_message(message)
        finally:
            self.consumer.close()

    def process_message(self, message):
        print(message)

    def shutdown(self):
        self.running = False
