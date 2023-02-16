import unittest
from xltdp.dal.mariadb.auth import Auth

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.auth = Authentication("localhost", "root", "password", "my_database")
        self.auth.connect()

    def test_connect(self):
        self.assertIsNotNone(self.auth.conn)
        self.assertIsNotNone(self.auth.cursor)

    def test_close(self):
        self.auth.close()
        self.assertIsNone(self.auth.conn)
        self.assertIsNone(self.auth.cursor)

    def tearDown(self):
        self.auth.close()

if __name__ == '__main__':
    unittest.main()