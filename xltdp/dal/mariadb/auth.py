import mariadb
import sys

class Auth:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database

    def connect(self):
        try:
            self.conn = mariadb.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor()

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB: {e}")
            sys.exit(1)

    def close(self):
        self.cursor.close()
        self.conn.close()