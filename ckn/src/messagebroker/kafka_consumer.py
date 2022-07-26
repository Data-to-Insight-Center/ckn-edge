from datetime import datetime
from json import loads
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from threading import current_thread
from ckn.src.util.graph_scripter import create_graph_request_from_json, create_graph_request_aggregated_json
from ckn.src.ingest.dbConnect import Database
from concurrent.futures import ThreadPoolExecutor

class KafkaCKNConsumer:

    def __init__(self, server_list, ckn_topic, db_uri, db_user, db_pwd, threadpool_size, max_poll_records, poll_timeout=1.0, group_id='group-ckn'):
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
            max_poll_records=max_poll_records,
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )
        self.db = Database(db_uri, db_user, db_pwd)
        self.executor = ThreadPoolExecutor(max_workers=threadpool_size)

    def consume(self):
        try:
            self.consumer.subscribe(self.topic)
            print("subscribing to topic ...")
            for message in self.consumer:
                self.executor.submit(self.process_message, message)
                # self.process_message(message.value)

        finally:
            self.consumer.close()

    def process_message(self, message):
        if message is None:
            print("Message is none")
            exit()
        else:
            request = create_graph_request_aggregated_json(message.value, 222)
            # self.db.run_cypher_query(request)
            print("thread: {} \t inserted cypher_query: {}".format(current_thread().name, request))

    def shutdown(self):
        self.running = False
