import sqlite3

conn = sqlite3.connect("todo.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
print("Users:", users)

cursor.execute("SELECT * FROM tasks")
tasks = cursor.fetchall()
print("Tasks:", tasks)

conn.close()