# ckn-edge


### How to run

#### Cloud system
This assumes you have docker installed. If not install docker via the [docker website](https://docs.docker.com/get-docker/)

1. Run the following in the cloud system directory to persist the graph DB
```shell
mkdir -p system_data/neo4j_data
```

3. Add the server IP to Kafka by changing the following in the docker-compose.yml file

```shell
KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092,PLAINTEXT_HOST://<SERVER_IP>:29092
```
4. Start the cloud system
```shell
docker compose up
```
3. Initialize the Kafka brokers for the required topics (for the incoming data)
```shell
sh ./init_scripts/create-kafka-topics.sh
```

4. Add Kafka Connect connector for Stream Sink (Replace the server IP)
```shell
curl -X POST http://<SERVER_IP>:8083/connectors \
  -H "Content-Type:application/json" \
  -H "Accept:application/json" \
  -d @sink.neo4j.json
```

6. Run the Kafka Stream processor (jar file)
