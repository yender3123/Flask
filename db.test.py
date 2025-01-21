import sqlite3

connection = sqlite3.connect('sqlite.db')
cursor = connection.cursor()

cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)",("заголовок", "контент"))

posts = cursor.fetchall()
print(posts)
connection.commit()
connection.close()
