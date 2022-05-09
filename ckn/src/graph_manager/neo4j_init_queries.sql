create (es:EdgeServer {name:'edge_server_1', bandwidth: '100Gbps', location: 'MESH_158A', status: "ACTIVE", created_at: DATETIME()});
create (es:EdgeServer {name:'edge_server_2', bandwidth: '100Gbps', location: 'MESH_158C', status: "ACTIVE", created_at: DATETIME()});
create (es:EdgeServer {name:'edge_server_3', bandwidth: '100Gbps', location: 'MESH_158B', status: "ACTIVE", created_at: DATETIME()});

create (ed:EdgeDevice {name:'raspi-1', location: 'MESH_158A', bandwidth: '10Gbps', status: "ACTIVE", created_at: DATETIME()});
create (ed:EdgeDevice {name:'raspi-2', location: 'MESH_158C', bandwidth: '10Gbps', status: "ACTIVE", created_at: DATETIME()});
create (ed:EdgeDevice {name:'raspi-3', location: 'MESH_158B', bandwidth: '20Gbps', status: "ACTIVE", created_at: DATETIME()});
create (ed:EdgeDevice {name:'jetson-1', location: 'MESH_158B', bandwidth: '20Gbps', status: "ACTIVE", created_at: DATETIME()});

match (es:EdgeServer {name:'edge_server_1'}) create (service:EdgeService {name: 'es_1_service_0', state: 'ACTIVE', state_changed: DATETIME()})-[r:HostedIn]->(es);
match (es:EdgeServer {name:'edge_server_2'}) create (service:EdgeService {name: 'es_2_service_0', state: 'ACTIVE', state_changed: DATETIME()})-[r:HostedIn]->(es);
match (es:EdgeServer {name:'edge_server_3'}) create (service:EdgeService {name: 'es_3_service_0', state: 'ACTIVE', state_changed: DATETIME()})-[r:HostedIn]->(es);

match (es:EdgeService {name:'es_1_service_0'}) create (model:ServiceModel {name: 'es_1_service_0_model_0', state: 'ACTIVE', state_changed: DATETIME()})-[r:AvailableFor]->(es);
match (es:EdgeService {name:'es_1_service_0'}) create (model:ServiceModel {name: 'es_1_service_0_model_1', state: 'ACTIVE', state_changed: DATETIME()})-[r:AvailableFor]->(es);
match (es:EdgeService {name:'es_1_service_0'}) create (model:ServiceModel {name: 'es_1_service_0_model_2', state: 'ACTIVE', state_changed: DATETIME()})-[r:AvailableFor]->(es);
match (es:EdgeService {name:'es_1_service_0'}) create (model:ServiceModel {name: 'es_1_service_0_model_3', state: 'INACTIVE', state_changed: DATETIME()})-[r:AvailableFor]->(es);
match (es:EdgeService {name:'es_1_service_0'}) create (model:ServiceModel {name: 'es_1_service_0_model_4', state: 'INACTIVE', state_changed: DATETIME()})-[r:AvailableFor]->(es);
match (es:EdgeService {name:'es_1_service_0'}) create (model:ServiceModel {name: 'es_1_service_0_model_5', state: 'ACTIVE', state_changed: DATETIME()})-[r:AvailableFor]->(es);

match (es:EdgeService {name:'es_2_service_0'}) create (model:ServiceModel {name: 'es_2_service_0_model_0', state: 'INACTIVE', state_changed: DATETIME()})-[r:AvailableFor]->(es);
match (es:EdgeService {name:'es_2_service_0'}) create (model:ServiceModel {name: 'es_2_service_0_model_1', state: 'INACTIVE', state_changed: DATETIME()})-[r:AvailableFor]->(es);
match (es:EdgeService {name:'es_2_service_0'}) create (model:ServiceModel {name: 'es_2_service_0_model_2', state: 'ACTIVE', state_changed: DATETIME()})-[r:AvailableFor]->(es);
match (es:EdgeService {name:'es_2_service_0'}) create (model:ServiceModel {name: 'es_2_service_0_model_3', state: 'ACTIVE', state_changed: DATETIME()})-[r:AvailableFor]->(es);
match (es:EdgeService {name:'es_2_service_0'}) create (model:ServiceModel {name: 'es_2_service_0_model_4', state: 'ACTIVE', state_changed: DATETIME()})-[r:AvailableFor]->(es);
match (es:EdgeService {name:'es_2_service_0'}) create (model:ServiceModel {name: 'es_2_service_0_model_5', state: 'ACTIVE', state_changed: DATETIME()})-[r:AvailableFor]->(es);

match (es:EdgeService {name:'es_3_service_0'}) create (model:ServiceModel {name: 'es_3_service_0_model_0', state: 'ACTIVE', state_changed: DATETIME()})-[r:AvailableFor]->(es);
match (es:EdgeService {name:'es_3_service_0'}) create (model:ServiceModel {name: 'es_3_service_0_model_1', state: 'INACTIVE', state_changed: DATETIME()})-[r:AvailableFor]->(es);
match (es:EdgeService {name:'es_3_service_0'}) create (model:ServiceModel {name: 'es_3_service_0_model_2', state: 'ACTIVE', state_changed: DATETIME()})-[r:AvailableFor]->(es);
match (es:EdgeService {name:'es_3_service_0'}) create (model:ServiceModel {name: 'es_3_service_0_model_3', state: 'ACTIVE', state_changed: DATETIME()})-[r:AvailableFor]->(es);
match (es:EdgeService {name:'es_3_service_0'}) create (model:ServiceModel {name: 'es_3_service_0_model_4', state: 'INACTIVE', state_changed: DATETIME()})-[r:AvailableFor]->(es);
match (es:EdgeService {name:'es_3_service_0'}) create (model:ServiceModel {name: 'es_3_service_0_model_5', state: 'INACTIVE', state_changed: DATETIME()})-[r:AvailableFor]->(es);
