import unittest
from xltdp.dal.mariadb.auth import Auth
from xltdp.dal.mariadb.database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.auth = Authentication("localhost", "root", "password", "my_database")
        self.auth.connect()
        self.db = Database(self.auth, "my_database")

    def test_create_database(self):
        self.db.create_database("my_new_database")
        self.assertIn("my_new_database", self.db.read_databases())

    def test_read_databases(self):
        self.assertIsInstance(self.db.read_databases(), list)

    def test_update_database(self):
        self.db.update_database("my_database_new")
        self.assertIn("my_database_new", self.db.read_databases())

    def test_delete_database(self):
        self.db.delete_database("my_database_new")
        self.assertNotIn("my_database_new", self.db.read_databases())

    def tearDown(self):
        self.auth.close()

if __name__ == '__main__':
    unittest.main()