STATE_MODEL_SERVICE = 'match(n:ServiceModel)-[r]->(m:EdgeService {{name: {} }}) where n.state={} return n'
