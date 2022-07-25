package org.d2i.ckn.model;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Data
@NoArgsConstructor
@AllArgsConstructor
public class AverageAggregator{
    private float average_accuracy = 0;
    private float average_delay = 0;
    private float total_events = 0;
    private String client_id = "";
    private String service_id = "";
    private String server_id = "";
    private long timestamp = 0;
}
