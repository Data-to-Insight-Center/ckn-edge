bash -c 'echo Waiting for Kafka to be ready... && \
                         kafka-topics --create --if-not-exists --topic inference-events --bootstrap-server broker:9092 && \
                         kafka-topics --create --if-not-exists --topic aggregated-events --bootstrap-server broker:9092'