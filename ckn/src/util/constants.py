INGEST_PROCESSED_REQUEST_TO_GRAPH = "MATCH (es:EdgeService {{name: '{0}'}}), (device:EdgeDevice{{name: '{1}'}})" \
                           " create (es)<-[r:Request {{ QoS:{2}, QoA:{3}, QoD:{4}, delay:{5}, delay_comm: {6}, " \
                          "delay_comp: {7}, model_id:'{8}', service_id: '{9}', req_id:{10}, created_time: TIMESTAMP()}}]-(device) return type(r);"

INGEST_REQUEST_TO_GRAPH = "MATCH (es:EdgeService {{name: '{0}'}}), (device:EdgeDevice{{name: '{1}'}})" \
                           " create (es)<-[r:Request {{ accuracy:{2}, delay:{3}, " \
                          "service_id: '{4}', req_id:{5}, added_time:TIMESTAMP(), created_time: TIMESTAMP()}}]-(device) return type(r);"


INGEST_AGGR_REQUEST_TO_GRAPH = "MATCH (es:EdgeServer {{name: '{0}'}}), (device:EdgeDevice{{name: '{1}'}})" \
                          " create (es)<-[r:WindowedRequest {{ device_id:'{1}', server_id:'{0}', avg_accuracy:{2}, avg_delay:{3}, " \
                          "service_id: '{4}', window_time:{5}, created_time: TIMESTAMP()}}]-(device) return type(r);"
