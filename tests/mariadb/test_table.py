import unittest
from xltdp.dal.mariadb.auth import Auth
from xltdp.dal.mariadb.database import Database
from xltdp.dal.mariadb.table import Table

class TestTable(unittest.TestCase):
    def setUp(self):
        self.auth = Auth("127.0.0.1", "root", "password", "my_database")
        self.auth.connect()
        self.db = Database(self.auth, "my_database")
        self.db.create_database("my_new_database")
        self.table = Table(self.auth, "my_database", "my_table")

    def test_create_table(self):
        self.table.create_table({"id": "INT", "name": "VARCHAR(255)", "email": "VARCHAR(255)"})
        self.assertIn("my_table", self.table.read_tables())

    def test_read_rows(self):
        self.table.create_table({"id": "INT", "name": "VARCHAR(255)", "email": "VARCHAR(255)"})
        self.table.create_row({"id": 1, "name": "John", "email": "john@example.com"})
        rows = self.table.read_rows("id = 1")
        self.assertIsInstance(rows, list)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], 1)
        self.assertEqual(rows[0][1], "John")
        self.assertEqual(rows[0][2], "john@example.com")

    def test_update_rows(self):
        self.table.create_table({"id": "INT", "name": "VARCHAR(255)", "email": "VARCHAR(255)"})
        self.table.create_row({"id": 1, "name": "John", "email": "john@example.com"})
        self.table.update_rows({"name": "Jane"}, "id = 1")
        rows = self.table.read_rows("id = 1")
        self.assertEqual(rows[0][1], "Jane")

    def test_delete_rows(self):
        self.table.create_table({"id": "INT", "name": "VARCHAR(255)", "email": "VARCHAR(255)"})
        self.table.create_row({"id": 1, "name": "John", "email": "john@example.com"})
        self.table.delete_rows("id = 1")
        rows = self.table.read_rows()
        self.assertEqual(len(rows), 0)

    def test_get_columns(self):
        self.table.create_table({"id": "INT", "name": "VARCHAR(255)", "email": "VARCHAR(255)"})
        columns = self.table.get_columns()
        self.assertIsInstance(columns, list)
        self.assertEqual(len(columns), 3)
        self.assertIn("id", columns)
        self.assertIn("name", columns)
        self.assertIn("email", columns)

    def test_clone_table(self):
        self.table.create_table({"id": "INT", "name": "VARCHAR(255)", "email": "VARCHAR(255)"})
        self.table.create_row({"id": 1, "name": "John", "email": "john@example.com"})
        self.table.clone_table("my_new_database.my_cloned_table")
        cloned_table = Table(self.auth, "my_new_database", "my_cloned_table")
        rows = cloned_table.read_rows()
        self.assertIsInstance(rows, list)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], 1)
        self.assertEqual(rows[0][1], "John")
        self.assertEqual(rows[0][2], "john@example.com")

    def test_update_table_add(self):
        self.table.create_table({"id": "INT", "name": "VARCHAR(255)", "email": "VARCHAR(255)"})
        self.table.update_table_add({"phone": "VARCHAR(255)"})
        columns = self.table.get_columns()
        self.assertIsInstance(columns, list)
        self.assertEqual(len(columns), 4)
        self.assertIn("id", columns)
        self.assertIn("name", columns)
        self.assertIn("email", columns)
        self.assertIn("phone", columns)

    def test_update_table_modify(self):
        self.table.create_table({"id": "INT", "name": "VARCHAR(255)", "email": "VARCHAR(255)"})
        self.table.update_table_modify({"name": "VARCHAR(50)"})
        columns = self.table.get_columns()
        self.assertIsInstance(columns, list)
        self.assertEqual(len(columns), 3)
        self.assertIn("id", columns)
        self.assertIn("name", columns)
        self.assertIn("email", columns)
        self.assertNotIn("name VARCHAR(255)", columns)
        self.assertIn("name VARCHAR(50)", columns)

    def test_update_table_drop(self):
        self.table.create_table({"id": "INT", "name": "VARCHAR(255)", "email": "VARCHAR(255)"})
        self.table.update_table_drop("email")
        columns = self.table.get_columns()
        self.assertIsInstance(columns, list)
        self.assertEqual(len(columns), 2)
        self.assertIn("id", columns)
        self.assertIn("name", columns)
        self.assertNotIn("email", columns)

    def tearDown(self):
        self.table.delete_table()
        self.db.delete_database("my_new_database")
        self.auth.close()

if __name__ == '__main__':
    unittest.main()
