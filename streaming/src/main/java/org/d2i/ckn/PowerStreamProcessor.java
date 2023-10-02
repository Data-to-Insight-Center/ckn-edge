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
import org.d2i.ckn.model.JsonSerde;
import org.d2i.ckn.model.power.CountSumAggregator;
import org.d2i.ckn.model.power.EventTimeExtractor;
import org.d2i.ckn.model.power.PowerEvent;
import org.d2i.ckn.model.power.AggregatedPowerEvent;

import java.io.IOException;
import java.io.InputStream;
import java.time.Duration;
import java.util.Properties;

@Slf4j
public class PowerStreamProcessor {

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
        try (InputStream input = PowerStreamProcessor.class.getClassLoader().getResourceAsStream("config.properties")) {
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
        Serde<PowerEvent> powerEventSerde = new JsonSerde<>(PowerEvent.class);
        Serde<CountSumAggregator> countSumAggregatorSerde = new JsonSerde<>(CountSumAggregator.class);
        Serde<AggregatedPowerEvent> averageAggregatorSerde = new JsonSerde<>(AggregatedPowerEvent.class);

        KStream<String, PowerEvent> powerEventKStream = streamsBuilder.stream(inputTopic,
                        Consumed.with(Serdes.String(), powerEventSerde)
                                .withTimestampExtractor(new EventTimeExtractor()));

        powerEventKStream.groupByKey()
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

    private static AggregatedPowerEvent process_average(CountSumAggregator value){
        long count = value.getCount();
        double avg_power = value.getPower_total()/count;
        return new AggregatedPowerEvent(avg_power, value.getClient_id(), value.getProcess_id(), value.getProcess_name(), System.currentTimeMillis());
    }

    private static StreamsBuilder getEdgeStreamsBuilder() {
        StreamsBuilder streamsBuilder = new StreamsBuilder();
        Serde<PowerEvent> powerEventSerde = new JsonSerde<>(PowerEvent.class);

        KStream<String, Long> inferenceEventKStream = streamsBuilder.stream(inputTopic,
                        Consumed.with(Serdes.String(), powerEventSerde))
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
