import unittest
from xltdp.dal.mariadb.auth import Auth
from xltdp.dal.mariadb.database import Database
from xltdp.dal.mariadb.table import Table
from xltdp.dal.mariadb.row import Row

class TestRow(unittest.TestCase):
    def setUp(self):
        self.auth = Authentication("localhost", "root", "password", "my_database")
        self.auth.connect()
        self.db = Database(self.auth, "my_database")
        self.table = Table(self.auth, "my_database", "my_table")
        self.row = Row(self.auth)

    def test_create_row(self):
        self.table.create_table({"id": "INT", "name": "VARCHAR(255)", "email": "VARCHAR(255)"})
        self.row.create_row("my_database.my_table", {"id": 1, "name": "John", "email": "john@example.com"})
        rows = self.table.read_rows()
        self.assertIsInstance(rows, list)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], 1)
        self.assertEqual(rows[0][1], "John")
        self.assertEqual(rows[0][2], "john@example.com")

    def test_read_row(self):
        self.table.create_table({"id": "INT", "name": "VARCHAR(255)", "email": "VARCHAR(255)"})
        self.row.create_row("my_database.my_table", {"id": 1, "name": "John", "email": "john@example.com"})
        rows = self.row.read_row("my_database.my_table", "id = 1")
        self.assertIsInstance(rows, list)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], 1)
        self.assertEqual(rows[0][1], "John")
        self.assertEqual(rows[0][2], "john@example.com")

    def test_update_row(self):
        self.table.create_table({"id": "INT", "name": "VARCHAR(255)", "email": "VARCHAR(255)"})
        self.row.create_row("my_database.my_table", {"id": 1, "name": "John", "email": "john@example.com"})
        self.row.update_row("my_database.my_table", {"name": "Jane"}, "id = 1")
        rows = self.row.read_row("my_database.my_table", "id = 1")
        self.assertEqual(rows[0][1], "Jane")

    def test_delete_row(self):
        self.table.create_table({"id": "INT", "name": "VARCHAR(255)", "email": "VARCHAR(255)"})
        self.row.create_row("my_database.my_table", {"id": 1, "name": "John", "email": "john@example.com"})
        self.row.delete_row("my_database.my_table", "id = 1")
        rows = self.table.read_rows()
        self.assertEqual(len(rows), 0)

    def tearDown(self):
        self.table.delete_table()
        self.db.delete_database("my_new_database")
        self.auth.close()

if __name__ == '__main__':
    unittest.main()
