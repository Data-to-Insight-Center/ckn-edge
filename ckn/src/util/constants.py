INGEST_REQUEST_TO_GRAPH = "MATCH (es:ServiceModel {{name: '{0}'}}), (device:EdgeDevice{{name: '{1}'}})" \
                           " create (es)<-[r:Request {{ QoS:{2}, QoA:{3}, QoD:{4}, delay:{5}, delay_comm: {6}, " \
                          "delay_comp: {7}, model_id:{8}, service_id: {9}, req_id:{10}, created_time: TIMESTAMP()}}]-(device) return type(r);"