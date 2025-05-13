from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os

import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a_very_secret_key_12345'


login_manager = LoginManager(app)
login_manager.login_view = 'login'

connection = sqlite3.connect("sqlite.db", check_same_thread=False)
cursor = connection.cursor()


def close_db(connection=None):
    if connection is not None:
        connection.close()

@app.teardown_appcontext
def close_connection(exception):
    close_db()

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def user_is_liking(user_id, post_id):
    like = cursor.execute(
        'SELECT * FROM like WHERE user_id = ? AND post_id = ?',
        (user_id, post_id)).fetchone()
    return bool(like)

@app.route('/like/<int:post_id>')
@login_required
def like_post(post_id):
    post = cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,)). fetchone()
    if post:
        if user_is_liking(current_user.id, post_id):
            cursor.execute('DELETE FROM  like WHERE user_id = ? AND post_id = ?', (current_user.id, post_id))
            connection.commit()
            print('You unliked this post.')
        else:
            cursor.execute('INSERT INTO like (user_id, post_id) VALUES (?, ?)', (current_user.id, post_id))
            connection.commit()
            print('You liked this post.')
        return redirect(url_for('index'))
    return 'Пост не найден. Вернитесь обратно', 404
@app.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def comment_post(post_id):
    post = cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    if post:
        text = request.form.get('comment_text')
        cursor.execute('INSERT INTO comments (user_id, post_id, comment_text) VALUES (?, ?, ?)',
                       (current_user.id, post_id, text))
        connection.commit()
        return redirect(url_for('index'))
    return 'Пост не найден. Вернитесь обратно', 404

@login_manager.user_loader
def load_user(user_id):
    user = cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if user is not None:
        return User(user[0], user[1], user[2])

    return None

@app.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    if post and post[3] == current_user.id:
        cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        print('Успешно')
        connection.commit()
        return redirect(url_for('index'))
    else:
        print('Проблема')
        return redirect(url_for('index'))
@app.route("/")
def index():
    cursor.execute('''  
        SELECT posts.id, posts.title, posts.content, posts.author_id, 
        users.username, COUNT(like.id) AS like FROM posts
        LEFT JOIN users ON posts.author_id = users.id
        LEFT JOIN like ON posts.id = like.post_id
        GROUP BY posts.id, posts.title, posts.content, posts.author_id, users.username
    ''')
    result = cursor.fetchall()
    posts = []
    for post in reversed(result):
        posts.append(
            {
                'id': post[0],
                'title': post[1],
                'content': post[2],
                'author_id': post[3],
                'username': post[4],
                'like': post[5]
            }
        )

    if current_user.is_authenticated:
        cursor.execute(
            'SELECT post_id FROM like WHERE user_id = ?', (current_user.id,)
        )
        likes_result = cursor.fetchall()
        liked_posts = [like[0] for like in likes_result]
        print(liked_posts)

        for post in posts:
            post['liked'] = post['id'] in liked_posts
        print(posts)
    context = {'posts': posts}
    return render_template('blog.html', **context)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        user = cursor.execute('SELECT * FROM users WHERE username =?', (username,)
        ).fetchone()
        if user and User(user[0], user[1], user[2]).check_password(password):
            login_user(User(user[0], user[1], user[2]))
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        # author_id = request.form['']
        cursor.execute(
            'INSERT INTO posts (title, content, author_id) VALUES(?, ?, ?)',
            (title, content, current_user.id)
        )
        connection.commit()
        return redirect(url_for('index'))
    return render_template('add_post.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                        (username, generate_password_hash(password))
            )
            print('Регистрация пользователя прошла успешно')
            return  redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('register.html',
                            message = 'Username already exists!')
    return render_template('register.html')

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
    post_one = cursor.execute('SELECT * FROM posts JOIN users ON posts.author_id = users.id WHERE posts.id = ?', (post_id,)).fetchone()
    comments = cursor.execute('''SELECT * FROM comments 
    JOIN users ON comments.user_id = users.id WHERE comments.post_id = ?''', (post_id,)).fetchall()
    print(comments)
    if post_one:
        post_dict = {
            'id': post_one[0],
            'title': post_one[1],
            'content': post_one[2],
            'author_id': post_one[3],
            'username': post_one[5]
        }
        comments_list = [{'id': comment[0], 'comment_text': comment[3], 'name': comment[6], 'time': comment[4]} for comment in comments]

        return render_template('post.html', post=post_dict, comments=comments_list)
    else:
        return "Пост не найден", 404



if __name__ == "__main__":
    app.run(debug=False, port=8080)