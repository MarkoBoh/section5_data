import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE users (id integer primary KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE items (store_id integer foreignkey, name text, price real)"
cursor.execute(create_table)

connection.commit()
connection.close()

