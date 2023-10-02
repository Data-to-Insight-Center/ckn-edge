package org.d2i.ckn.model.power;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Data
@NoArgsConstructor
@AllArgsConstructor
public class AggregatedPowerEvent{
    private double average_power_consumption = 0;
    private String client_id = "";
    private long process_id = 0;
    private String process_name = "";
    private long timestamp = 0;
}
