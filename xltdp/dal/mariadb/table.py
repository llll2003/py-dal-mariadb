import mysql.connector

class Table:
    def __init__(self, auth, database):
        self.auth = auth
        self.database = database
        self.auth.connect()

    def create_table(self, name, columns):
        column_definitions = ", ".join([f"{name} {datatype}" for name, datatype in columns.items()])
        query = f"CREATE TABLE {self.database}.{name} ({column_definitions})"
        self.auth.cursor.execute(query)
        self.auth.conn.commit()

    def read_tables(self):
        query = f"SHOW TABLES FROM {self.database}"
        self.auth.cursor.execute(query)
        return [table[0] for table in self.auth.cursor.fetchall()]

    def delete_table(self, name):
        query = f"DROP TABLE {self.database}.{name}"
        self.auth.cursor.execute(query)
        self.auth.conn.commit()

    def update_table_add(self, name, columns):
        current_columns = self.get_columns(name)
        column_definitions = ", ".join([f"{name} {datatype}" for name, datatype in columns.items() if name not in current_columns])
        if column_definitions:
            query = f"ALTER TABLE {self.database}.{name} ADD COLUMN {column_definitions}"
            self.auth.cursor.execute(query)
            self.auth.conn.commit()
    
    def update_table_modify(self, name, columns):
        current_columns = self.get_columns(name)
        for name, datatype in columns.items():
            if name in current_columns:
                query = f"ALTER TABLE {self.database}.{name} MODIFY COLUMN {name} {datatype}"
                self.auth.cursor.execute(query)
                self.auth.conn.commit()

    def update_table_drop(self, name, columns):
        current_columns = self.get_columns(name)
        for name in columns:
            if name in current_columns:
                query = f"ALTER TABLE {self.database}.{name} DROP COLUMN {name}"
                self.auth.cursor.execute(query)
                self.auth.conn.commit()

    def clone_table(self, original_name, new_name):
        original_database, original_table = original_name.split(".")
        new_database, new_table = new_name.split(".")
        query = f"CREATE TABLE {new_database}.{new_table} LIKE {original_database}.{original_table}"
        self.auth.cursor.execute(query)
        self.auth.conn.commit()

    def get_columns(self, name):
        query = f"SHOW COLUMNS FROM {self.database}.{name}"
        self.auth.cursor.execute(query)
        return [column[0] for column in self.auth.cursor.fetchall()]

    def __del__(self):
        self.auth.close()
