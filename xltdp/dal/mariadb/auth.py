import mysql.connector

class Auth:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()
