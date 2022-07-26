package org.d2i.ckn;

import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.utils.Bytes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.KeyValue;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.*;
import org.apache.kafka.streams.state.WindowStore;
import org.d2i.ckn.model.*;

import java.io.IOException;
import java.io.InputStream;
import java.time.Duration;
import java.util.Properties;

@Slf4j
public class StreamProcessor {

    private static String inputTopic;
    private static String outputTopic;
    private static String countSumStore;
    private static String groupId;
    private static String bootstrapServers;
    private static String processorClientId;
    private static long timeWindowSize;
    private static int windowGracePeriod;
    public static void main(String[] args) {
        // load the configurations
        try (InputStream input = StreamProcessor.class.getClassLoader().getResourceAsStream("config.properties")) {
            Properties config = new Properties();
            if (input == null) {
                log.error("The configuration file could not be found!");
                return;
            }
            config.load(input);

            inputTopic = config.getProperty("stream.input.topic");
            outputTopic = config.getProperty("stream.output.topic");
            countSumStore = config.getProperty("stream.aggr.store");
            groupId = config.getProperty("stream.group.id");
            bootstrapServers = config.getProperty("stream.kafka.servers");
            processorClientId = config.getProperty("stream.kafka.clientId");
            timeWindowSize = Long.parseLong(config.getProperty("stream.kafka.windowSize"));
            windowGracePeriod = Integer.parseInt(config.getProperty("stream.kafka.window.gracePeriod"));

        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        // setup Stream processing properties
        Properties streamsProps = getProperties();

        // building the stream processing topology
        StreamsBuilder builder = getWindowedAggregationBuilder();

        // starting the stream processor
        KafkaStreams kafkaStreams = new KafkaStreams(builder.build(), streamsProps);
        kafkaStreams.start();
    }

    private static StreamsBuilder getWindowedAggregationBuilder() {
        StreamsBuilder streamsBuilder = new StreamsBuilder();
        Serde<InferenceEvent> inferenceEventSerde = new JsonSerde<>(InferenceEvent.class);
        Serde<CountSumAggregator> countSumAggregatorSerde = new JsonSerde<>(CountSumAggregator.class);
        Serde<AverageAggregator> averageAggregatorSerde = new JsonSerde<>(AverageAggregator.class);

        KStream<String, InferenceEvent> inferenceEventKStream = streamsBuilder.stream(inputTopic,
                        Consumed.with(Serdes.String(), inferenceEventSerde)
                                .withTimestampExtractor(new EventTimeExtractor()));

        // todo: tumbling or sliding window?
        inferenceEventKStream.groupByKey()
                .windowedBy(TimeWindows.of(Duration.ofSeconds(timeWindowSize)).grace(Duration.ofSeconds(windowGracePeriod)))
                .aggregate(CountSumAggregator::new,
                        (key, value, aggregate) -> aggregate.process(value),
                        Materialized.<String, CountSumAggregator, WindowStore<Bytes, byte[]>>as(countSumStore)
                                .withKeySerde(Serdes.String())
                                .withValueSerde(countSumAggregatorSerde)
                )
                .suppress(Suppressed.untilWindowCloses(Suppressed.BufferConfig.unbounded()))
                .toStream()
                .map((Windowed<String>winKey, CountSumAggregator value) -> {
                    return new KeyValue<>(winKey.key(), process_average(value));
                })
                .peek((key, value) -> log.info("Outgoing record - key " +key +" value " + value))
                .to(outputTopic, Produced.with(Serdes.String(), averageAggregatorSerde));

        return streamsBuilder;
    }

    private static AverageAggregator process_average(CountSumAggregator value){
        long count = value.getCount();
        float average_accuracy = value.getAccuracy_total()/count;
        float average_delay = value.getDelay_total()/count;
        return new AverageAggregator(average_accuracy, average_delay, count, value.getClient_id(), value.getService_id(), value.getServer_id(), System.currentTimeMillis());
    }

    private static StreamsBuilder getEdgeStreamsBuilder() {
        StreamsBuilder streamsBuilder = new StreamsBuilder();
        Serde<InferenceEvent> inferenceEvents = new JsonSerde<>(InferenceEvent.class);

        KStream<String, Long> inferenceEventKStream = streamsBuilder.stream(inputTopic,
                        Consumed.with(Serdes.String(), inferenceEvents))
//                .peek((key, value) -> System.out.println("Outgoing record - key " +key +" value " + value.getClient_id() + "\taccuracy" + value.getAccuracy()))
                .groupByKey()
                .count()
                .toStream()
                .peek((key, value) -> System.out.println("Outgoing record - key " +key +" value " + value));

        return streamsBuilder;
    }

    private static Properties getProperties() {
        Properties configuration = new Properties();
        configuration.put(StreamsConfig.APPLICATION_ID_CONFIG, groupId);
        configuration.put(StreamsConfig.CLIENT_ID_CONFIG, processorClientId);
        configuration.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        configuration.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        configuration.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
//        configuration.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        configuration.setProperty(StreamsConfig.COMMIT_INTERVAL_MS_CONFIG, String.valueOf(1*1000));
        return configuration;
    }
}
