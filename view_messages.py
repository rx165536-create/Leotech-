import sqlite3

conn = sqlite3.connect("leotech.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM contacts")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
