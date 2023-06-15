/* get the latest deployed model on Edge server 1*/
MATCH (es:EdgeServer {name: "EDGE-1"})<-[d:DEPLOYED_IN]-(ai:AIModel)
with es, d, ai order by d.changed_at  DESC return es.name, ai.name, d.changed_at as lastTimestamp limit 1