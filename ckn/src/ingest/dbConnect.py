from neo4j import GraphDatabase

class Database(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    def close(self):
        self._driver.close()

    def run_cypher_query(self, query):
        """
        Runs a given query
        :param query:
        :return:
        """
        with self._driver.session() as session:
            session.write_transaction(self.add_input_graph, query)

    def add_property_to_node(self, query):
        """
        Adds an input to the graph
        :param query:
        :return:
        """
        with self._driver.session() as session:
            session.write_transaction(self.add_property_to_graph, query)

    def add_user(self, name):
        with self._driver.session() as session:
            session.write_transaction(self.create_user_node, name)
            return session.read_transaction(self.match_user_node, name)

    # Units of work

    def print_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

    @staticmethod
    def create_user_node(tx, name):
        return tx.run(CREATE_USER, name=name).single().value()

    @staticmethod
    def match_user_node(tx, name):
        result = tx.run(READ_USER, name=name)
        return result.single()[0]

    @staticmethod
    def run_init_fobs_graph(tx, query):
        return tx.run(query).single()

    @staticmethod
    def add_input_graph(tx, query):
        return tx.run(query).single()

    @staticmethod
    def add_property_to_graph(tx, query):
        return tx.run(query).single()

