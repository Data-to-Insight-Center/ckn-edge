create (es:EdgeServer {name:'edge_server_3', bandwidth: '100Gbps', location: 'MESH_158C', status: "ACTIVE"})

create (ed:EdgeDevice {name:'raspi-3', location: 'MESH_158A', bandwidth: '10Gbps', status: "ACTIVE"})

match (es:EdgeServer {name:'edge_server_2'})
create (service:EdgeService {name: 'es_2_service_0'})-[r:HostedIn]->(es)

match (es:EdgeService {name:'es_2_service_0'})
create (model:ServiceModel {name: 'es_2_service_0_model_3'})-[r:AvailableFor]->(es)

