import mysql.connector

class Database:
    def __init__(self, auth):
        self.auth = auth
        self.auth.connect()

    def create_database(self, name):
        query = f"CREATE DATABASE {name}"
        self.auth.cursor.execute(query)

    def read_databases(self):
        query = "SHOW DATABASES"
        self.auth.cursor.execute(query)
        return [database[0] for database in self.auth.cursor.fetchall()]

    def delete_database(self, name):
        query = f"DROP DATABASE {name}"
        self.auth.cursor.execute(query)

    def __del__(self):
        self.auth.close()
