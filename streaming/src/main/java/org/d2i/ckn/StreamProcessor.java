package org.d2i.ckn;

import lombok.extern.log4j.Log4j;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.Produced;
import org.d2i.ckn.model.InferenceEvent;
import org.d2i.ckn.model.JsonSerde;

import java.util.Locale;
import java.util.Properties;

@Slf4j
public class StreamProcessor {

    private static String inputTopic = "inference-requests2";
    private static String outputTopic = "order-out";

    public static void main(String[] args) {
        Properties streamsProps = getProperties();

        StreamsBuilder builder = getEdgeStreamsBuilder();

        KafkaStreams kafkaStreams = new KafkaStreams(builder.build(), streamsProps);

        kafkaStreams.start();
    }

    private static StreamsBuilder getWindowedAggregationBuilder() {
        StreamsBuilder streamsBuilder = new StreamsBuilder();
        Serde<InferenceEvent> inferenceEvents = new JsonSerde<>(InferenceEvent.class);

        KStream<String, Long> inferenceEventKStream = streamsBuilder.stream(inputTopic,
                        Consumed.with(Serdes.String(), inferenceEvents))
                .peek((key, value) -> System.out.println("Outgoing record - key " +key +" value " + value.getClient_id() + "\taccuracy" + value.getAccuracy()))
                .groupBy((key, value) -> value.getClient_id())
                .count()
                .toStream()
                .peek((key, value) -> System.out.println("Outgoing record - key " +key +" value " + value));

        return streamsBuilder;
    }

    private static StreamsBuilder getEdgeStreamsBuilder() {
        StreamsBuilder streamsBuilder = new StreamsBuilder();
        Serde<InferenceEvent> inferenceEvents = new JsonSerde<>(InferenceEvent.class);

        KStream<String, Long> inferenceEventKStream = streamsBuilder.stream(inputTopic,
                        Consumed.with(Serdes.String(), inferenceEvents))
                .peek((key, value) -> System.out.println("Outgoing record - key " +key +" value " + value.getClient_id() + "\taccuracy" + value.getAccuracy()))
                .groupBy((key, value) -> value.getClient_id())
                .count()
                .toStream()
                .peek((key, value) -> System.out.println("Outgoing record - key " +key +" value " + value));

        return streamsBuilder;
    }

    private static Properties getProperties() {
        String groupId = "test-group-3";
        String bootstrapServers = "localhost:9092";
        String clientId = "java-test-client2";

        Properties configuration = new Properties();
        configuration.put(StreamsConfig.APPLICATION_ID_CONFIG, groupId);
        configuration.put(StreamsConfig.CLIENT_ID_CONFIG, clientId);
        configuration.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        configuration.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        configuration.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
//        configuration.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        configuration.setProperty(StreamsConfig.COMMIT_INTERVAL_MS_CONFIG, String.valueOf(1*1000));
        return configuration;
    }
}
