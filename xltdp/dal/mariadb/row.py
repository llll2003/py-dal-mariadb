import mysql.connector

class Row:
    def __init__(self, auth, database, table):
        self.auth = auth
        self.database = database
        self.table = table
        self.auth.connect()

    def create_row(self, data):
        keys = ", ".join(data.keys())
        values = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {self.database}.{self.table} ({keys}) VALUES ({values})"
        values_tuple = tuple(data.values())
        self.auth.cursor.execute(query, values_tuple)
        self.auth.conn.commit()

    def read_rows(self, condition=None):
        query = f"SELECT * FROM {self.database}.{self.table}"
        if condition:
            query += f" WHERE {condition}"
        self.auth.cursor.execute(query)
        return self.auth.cursor.fetchall()

    def update_row(self, data, condition):
        set_clause = ", ".join([f"{k} = %s" for k in data.keys()])
        query = f"UPDATE {self.database}.{self.table} SET {set_clause} WHERE {condition}"
        values_tuple = tuple(data.values())
        self.auth.cursor.execute(query, values_tuple)
        self.auth.conn.commit()

    def delete_row(self, condition):
        query = f"DELETE FROM {self.database}.{self.table} WHERE {condition}"
        self.auth.cursor.execute(query)
        self.auth.conn.commit()

    def __del__(self):
        self.auth.close()
