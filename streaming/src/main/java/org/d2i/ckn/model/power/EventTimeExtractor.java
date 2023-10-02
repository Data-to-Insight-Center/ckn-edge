package org.d2i.ckn.model.power;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.streams.processor.TimestampExtractor;
import org.d2i.ckn.model.qoe.InferenceEvent;

import java.util.Optional;

public class EventTimeExtractor implements TimestampExtractor {
    @Override
    public long extract(ConsumerRecord<Object, Object> consumerRecord, long partitionTime) {
        PowerEvent powerEvent = (PowerEvent) consumerRecord.value();
        return Optional.ofNullable(powerEvent.getTimestamp())
                .map(at -> at.toInstant().toEpochMilli())
                .orElse(partitionTime);
    }
}
