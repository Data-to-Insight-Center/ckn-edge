# ckn-edge


### How to run

#### Cloud system
This assumes you have docker installed. If not install docker via the [docker website](https://docs.docker.com/get-docker/)

1. Run the following in the cloud system directory to persist the graph DB
```shell
mkdir -p system_data/neo4j_data
```

2. Add the server IP to Kafka by changing the following in the docker-compose.yml file

```shell
KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092,PLAINTEXT_HOST://<SERVER_IP>:29092
```
3. Start the cloud system
```shell
docker compose up
```
4. Initialize the Kafka brokers for the required topics (for the incoming data)
```shell
sh ./init_scripts/create-kafka-topics.sh
```

5. Add Kafka Connect connector for Aggregator Stream sink (Replace the server IP)
```shell
curl -X POST http://<SERVER_IP>:8083/connectors \
  -H "Content-Type:application/json" \
  -H "Accept:application/json" \
  -d @aggregated_sink.neo4j.json
```

6. Add Kafka Connect connector for Server state sink (Replace the server IP)
```shell
curl -X POST http://<SERVER_IP>:8083/connectors \
  -H "Content-Type:application/json" \
  -H "Accept:application/json" \
  -d @model_sink.neo4j.json
```

7. Run the Kafka Stream processor (jar file)
```shell
java -jar ckn-streaming-1.0-SNAPSHOT-jar-with-dependencies.jar
```