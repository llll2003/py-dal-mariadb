from xltdp.dal.mariadb.auth import Auth
from xltdp.dal.mariadb.database import Database
from xltdp.dal.mariadb.table import Table
from xltdp.dal.mariadb.row import Row

auth = Auth("127.0.0.1", "root", "password", "mysql")
database = Database(auth)
table = Table(auth, "mysql")

try:
   # Create a new table with two columns
   table.create_table("mytable", {"id": "INT", "name": "VARCHAR(255)"})
except BaseException:
   # Delete the table
   table.delete_table("mytable")
   table.create_table("mytable", {"id": "INT", "name": "VARCHAR(255)"})
   pass

row = Row(auth, "mysql", "mytable")

# Insert a new row into the table
row.create_row({"id": 1, "name": "Alice"})

# Read all rows from the table
rows = row.read_rows()
print(rows)

# Update the name of the first row
row.update_row({"name": "Bob"}, "id = 1")

# Delete the first row
row.delete_row("id = 1")

# Add a new column to the table
table.update_table_add("mytable", {"age": "INT"})

# Modify the data type of a column in the table
table.update_table_modify("mytable", {"age": "VARCHAR(255)"})

# Drop a column from the table
table.update_table_drop("mytable", ["age"])

# Clone the table
table.clone_table("mysql.mytable", "mysql.mytable_clone")

# Delete the table
table.delete_table("mytable")

# Create a new database
database.create_database("mynewdatabase")

# Read all databases
databases = database.read_databases()
print(databases)

# Delete the database
database.delete_database("mynewdatabase")