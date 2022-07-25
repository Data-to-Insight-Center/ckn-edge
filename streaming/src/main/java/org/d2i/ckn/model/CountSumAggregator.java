package org.d2i.ckn.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Data
@NoArgsConstructor
@AllArgsConstructor
public class CountSumAggregator{
    private long count = 0;
    private float accuracy_total = 0;
    private float delay_total = 0;
    private String client_id = "2";
    private String service_id = "2";
    private String server_id = "2";

    public CountSumAggregator process(InferenceEvent inferenceEvent) {
        this.client_id = inferenceEvent.getClient_id();
        this.service_id = inferenceEvent.getService_id();
        this.server_id = inferenceEvent.getServer_id();
        this.count++;
        this.accuracy_total += inferenceEvent.getAccuracy();
        this.delay_total += inferenceEvent.getDelay();
//        log.info(this.toString());
        return this;
    }
}
