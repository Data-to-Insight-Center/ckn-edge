import unittest
from ckn.src.ingest.dbConnect import Database


class DBConnectionTest(unittest.TestCase):
    @classmethod
    def test_connection(cls):
        db_user = "neo4j"
        db_uri = "bolt://172.28.96.1:11003"
        # db_uri = "bolt://192.168.86.178:11003"
        db_pwd = "root"

        db = Database(db_uri, db_user, db_pwd)
        db.print_greeting("Hello World")
        db.close()


if __name__ == '__main__':
    unittest.main()
