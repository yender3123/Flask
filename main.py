from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("sqlite.db")
    conn.row_factory = sqlite3.Row
    return conn

def close_db(conn):
    if conn:
        conn.close()

@app.teardown_appcontext
def close_connection(exception):
    conn = get_db_connection()
    close_db(conn)

@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * from posts')
    result = cursor.fetchall()
    posts = []
    for post in reversed(result):
        posts.append(
            {'id': post['id'], 'title': post['title'], 'content': post['content']}
        )
    close_db(conn)
    context = {'posts': posts}
    return render_template('blog.html', **context)

@app.route('/add', methods=['GET', 'POST'])
def add_post():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute(
            'INSERT INTO posts (title, content) VALUES(?, ?)',
            (title, content)
        )
        conn.commit()
        close_db(conn)
        return redirect(url_for('index'))
    close_db(conn)
    return render_template('add_post.html')

@app.route("/number/<int:number>")
def say_number(number):
    return f"Ты выбрал число {number}"

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

@app.route('/post/<int:post_id>')
def post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    post_one = cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    close_db(conn)
    if post_one:
        post_dict = {'id': post_one['id'], 'title': post_one['title'], 'content': post_one['content']}
        return render_template('post.html', post=post_dict)
    else:
        return "Пост не найден", 404


if __name__ == "__main__":
    app.run(debug=False, port=8080)