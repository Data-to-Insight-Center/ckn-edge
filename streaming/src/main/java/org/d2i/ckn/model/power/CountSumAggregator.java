package org.d2i.ckn.model.power;

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
    private double power_total = 0;
    private String client_id = "";
    private long process_id = 0;
    private String process_name = "";

    public CountSumAggregator process(PowerEvent powerEvent) {
        this.client_id = powerEvent.getClient_id();
        this.count++;
        this.process_id = powerEvent.getProcess_id();
        this.process_name = powerEvent.getProcess_name();
        this.power_total += powerEvent.getPower_consumption();
        return this;
    }
}
