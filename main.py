from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

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

if __name__ == "__main__":
    app.run()