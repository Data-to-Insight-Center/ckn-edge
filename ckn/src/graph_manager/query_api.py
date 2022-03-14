from ckn.src.graph_manager.query_templates import STATE_MODEL_SERVICE

def retrieve_state_models(graph, service_id, state="ACTIVE"):
    query = STATE_MODEL_SERVICE.format(service_id, state)
    graph.run_cypher_query(query)