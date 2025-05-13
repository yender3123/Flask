import sqlite3

connection = sqlite3.connect('../sqlite.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        comment_text TEXT NOT NULL,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP); ''')

connection.commit()
connection.close()