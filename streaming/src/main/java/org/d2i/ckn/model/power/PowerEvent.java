package org.d2i.ckn.model.power;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.d2i.ckn.model.EdgeEvent;

import java.util.Date;

@Data
@NoArgsConstructor
@Builder
@AllArgsConstructor
public class PowerEvent implements EdgeEvent {
    private String client_id;
    private long process_id;
    private String process_name;
    private double power_consumption;
    @JsonFormat(shape = JsonFormat.Shape.STRING,
            pattern = "yyyy-MM-dd hh:mm:ss")
    private Date timestamp;
}
