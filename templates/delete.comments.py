import sqlite3

connection = sqlite3.connect('../sqlite.db')
cursor = connection.cursor()

cursor.execute('''
    DROP TABLE comments ''')

connection.commit()
connection.close()