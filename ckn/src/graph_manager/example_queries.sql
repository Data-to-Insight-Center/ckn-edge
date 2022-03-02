# average query
match (m:ServiceModel)<-[r:Request]-(d:device)
return m.name as recv_model, d.name as sent_model, avg(r.delay) as avg_delay, avg(r.QoD) as avg_QoD

# forwarding requests
match (m:ServiceModel {name: 'es_1_service_0_model_1'})<-[r:Request]-(d:EdgeDevice {name: 'raspi-1'})
where r.delay < 0.0001 AND r.QoA < 0.8
create (m)-[r2:ForwardRequest {QoA: r.QoA, QoD: r.QoD, model: r.model_id, delay: r.delay, delay_comm: r.delay_comm, forward_time: DATETIME(), created_time: r.created_time}]->(m2:ServiceModel{name: 'es_2_service_0_model_1'})
return count(*);