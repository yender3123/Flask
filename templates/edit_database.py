import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
connection = sqlite3.connect('../sqlite.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL); ''')

cursor.execute('ALTER TABLE posts ADD author_id INTEGER;')



cursor.execute('INSERT INTO users VALUES (?, ?, ?)',
               (1, 'Rocket', generate_password_hash('qwerty123')))

cursor.execute('UPDATE posts SET author_id = 1;')

connection.commit()
connection.close()