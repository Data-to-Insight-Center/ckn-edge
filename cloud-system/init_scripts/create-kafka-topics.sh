docker exec -it broker kafka-topics --create --if-not-exists --topic inference-qoe-test --bootstrap-server broker:9092
docker exec -it broker kafka-topics --create --if-not-exists --topic aggregate-events --bootstrap-server broker:9092
docker exec -it broker kafka-topics --create --if-not-exists --topic model-deployments --bootstrap-server broker:9092