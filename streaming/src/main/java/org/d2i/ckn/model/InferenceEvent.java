package org.d2i.ckn.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;

@Data
@NoArgsConstructor
@Builder
@AllArgsConstructor
public class InferenceEvent implements EdgeEvent{
    private String server_id;
    private String service_id;
    private String client_id;
//    private Date added_time;
    private float delay;
    private float accuracy;
}
