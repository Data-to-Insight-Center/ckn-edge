from ckn.src.messagebroker.kafka_consumer import KafkaCKNConsumer

def main():
    FILE = "/mnt/d/git/ckn-edge/ckn/test/ingest/resources/qos_pred_sample.csv"
    # FILE = "D:/git/ckn-edge/ckn/test/ingest/resources/qos_pred_raspi-2-es2.csv"
    DB_USER = "neo4j"
    DB_URI = "bolt://192.168.86.178:11003"
    DB_PWD = "root"
    KAFKA_TOPIC = "inf-events"
    server_list = ['localhost:9092']

    consumer = KafkaCKNConsumer(KAFKA_TOPIC, server_list)
    consumer.consume()

if __name__ == "__main__":
    main()