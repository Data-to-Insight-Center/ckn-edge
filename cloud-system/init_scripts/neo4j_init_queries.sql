create (es:EdgeServer {name:'EDGE-1', bandwidth: '100Gbps', location: 'MESH_158A', status: 'ACTIVE'});
create (es:EdgeServer {name:'EDGE-2', bandwidth: '100Gbps', location: 'MESH_158C', status: 'ACTIVE'});
create (es:EdgeServer {name:'EDGE-3', bandwidth: '100Gbps', location: 'MESH_158B', status: 'ACTIVE'});

create (ed:EdgeDevice {name:'raspi-1', location: 'MESH_158A', bandwidth: '10Gbps', status: 'ACTIVE'});
create (ed:EdgeDevice {name:'raspi-2', location: 'MESH_158C', bandwidth: '10Gbps', status: 'ACTIVE'});
create (ed:EdgeDevice {name:'raspi-3', location: 'MESH_158B', bandwidth: '10Gbps', status: 'ACTIVE'});
create (ed:EdgeDevice {name:'raspi-4', location: 'MESH_158B', bandwidth: '20Gbps', status: 'ACTIVE'});
create (ed:EdgeDevice {name:'raspi-5', location: 'MESH_158B', bandwidth: '20Gbps', status: 'ACTIVE'});

create (service:Service {name: 'imagenet_image_classification', state: 'ACTIVE', state_changed: DATETIME()});
create (service:Service {name: 'animal_sound_identification', state: 'ACTIVE', state_changed: DATETIME()});
create (service:Service {name: 'car_detection', state: 'ACTIVE', state_changed: DATETIME()});


create (ai:AIModel {name:'shufflenet_v2_x0_5', accuracy: 0.5017682318647425, latency: 0.013298789718443163, location: "torch.hub.load(''pytorch/vision:v0.10.0'', ''squeezenet1_1'', pretrained=True)", type: 'cnn'});
create (ai:AIModel {name:'densenet201', accuracy: 0.4602605871345783, latency: 0.13881205862710908, location: "torch.hub.load(''pytorch/vision:v0.10.0'', ''squeezenet1_1'', pretrained=True)", type: 'cnn'});
create (ai:AIModel {name:'googlenet', accuracy: 0.32817536894549254, latency: 0.05995039339791403, location: "torch.hub.load(''pytorch/vision:v0.10.0'', ''squeezenet1_1'', pretrained=True)", type: 'cnn'});
create (ai:AIModel {name:'mobilenet_v3_small', accuracy: 0.4755329001730449, latency: 0.011956614513914936, location: "torch.hub.load(''pytorch/vision:v0.10.0'', ''squeezenet1_1'', pretrained=True)", type: 'cnn'});
create (ai:AIModel {name:'resnet152', accuracy: 0.4953759648061317, latency: 0.20684462207296617, location: "torch.hub.load(''pytorch/vision:v0.10.0'', ''squeezenet1_1'', pretrained=True)", type: 'cnn'});
create (ai:AIModel {name:'resnext50_32x4d', accuracy: 0.5381981524117827, latency: 0.09525601770009709, location: "torch.hub.load(''pytorch/vision:v0.10.0'', ''squeezenet1_1'', pretrained=True)", type: 'cnn'});
create (ai:AIModel {name:'squeezenet1_1', accuracy: 0.46608824045246044, latency: 0.020633205696133455, location: "torch.hub.load(''pytorch/vision:v0.10.0'', ''squeezenet1_1'', pretrained=True)", type: 'cnn'});


match (ai:AIModel {name:'shufflenet_v2_x0_5'}) match (service:Service {name: 'imagenet_image_classification'}) create (ai)-[r:ModelOf]->(service);
match (ai:AIModel {name:'densenet201'}) match (service:Service {name: 'imagenet_image_classification'}) create (ai)-[r:ModelOf]->(service);
match (ai:AIModel {name:'googlenet'}) match (service:Service {name: 'imagenet_image_classification'}) create (ai)-[r:ModelOf]->(service);
match (ai:AIModel {name:'mobilenet_v3_small'}) match (service:Service {name: 'imagenet_image_classification'}) create (ai)-[r:ModelOf]->(service);
match (ai:AIModel {name:'resnet152'}) match (service:Service {name: 'imagenet_image_classification'}) create (ai)-[r:ModelOf]->(service);
match (ai:AIModel {name:'resnext50_32x4d'}) match (service:Service {name: 'imagenet_image_classification'}) create (ai)-[r:ModelOf]->(service);
match (ai:AIModel {name:'squeezenet1_1'}) match (service:Service {name: 'imagenet_image_classification'}) create (ai)-[r:ModelOf]->(service);



-- match (es:EdgeServer {name:'EDGE-1'}) match (service:Service {name: 'imagenet_image_classification'}) create (service)-[r:HostedIn]->(es);
-- match (es:EdgeServer {name:'EDGE-2'}) match (service:Service {name: 'imagenet_image_classification'}) create (service)-[r:HostedIn]->(es);
-- match (es:EdgeServer {name:'EDGE-3'}) match (service:Service {name: 'imagenet_image_classification'}) create (service)-[r:HostedIn]->(es);
-- match (es:EdgeServer {name:'EDGE-2'}) match (service:Service {name: 'car_detection'}) create (service)-[r:HostedIn]->(es);
-- match (es:EdgeServer {name:'EDGE-3'}) match (service:Service {name: 'animal_sound_identification'}) create (service)-[r:HostedIn]->(es);
