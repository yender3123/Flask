from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()

def close_db(connection=None):
    if connection is not None:
        connection.close()

@app.teardown_appcontext
def close_connection(exception):
    close_db()

@app.route("/")
def index():
    cursor.execute('SELECT * from posts')
    result = cursor.fetchall()
    posts = []
    for post in result:
        posts.append(
            {'id': post[0], 'title': post[1], 'content': post[2]}
        )
    context = {'posts': posts}
    return render_template('blog.html', **context)

@app.route("/Mark")
def mark_name():
    return "Привет, Марк"

# @app.route("/Den")
# def den_name():
#     return "Привет, Ден"

@app.route("/Vlad")
def vlad_name():
    return render_template('Vlad.html')

@app.route('/power')
def power_name():
    return str(2**10)

@app.route('/<name>')
def say_name(name):
    return f'Ты выбрал имя {name.capitalize()}'

@app.route("/blog")
def blog():
    context = {
        'posts': [
            {
                'heading': 'Путешествие в горы',
                'content': 'В этом посте я расскажу о своем недавнем походе в горы, о красоте природы и о том, как важно проводить время на свежем воздухе.',
                'date': '2025-03-12'
            },
            {
                'heading': 'Кулинарные эксперименты',
                'content': 'Делюсь рецептом необычного блюда, которое я приготовил на выходных. Это сочетание ингредиентов удивило моих друзей!',
                'date': '2024-03-12'
            },
            # {
            #     'heading': 'Чтение книг в эпоху технологий',
            #     'content': 'Обсуждаю, как чтение книг остается актуальным в современном мире, несмотря на все новые технологии и гаджеты.',
            #     'date': '2023-03-12'
            # },
        ]
    }
    return render_template('blog.html', **context)

if __name__ == "__main__":
    app.run()