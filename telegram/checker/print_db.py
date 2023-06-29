import sqlite3

conn = sqlite3.connect('messages.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    print(f"Table: {table_name}")
    cursor.execute(f'SELECT * FROM "{table_name}";')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print()  

conn.close()

