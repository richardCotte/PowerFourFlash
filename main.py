from importlib.resources import path
from flask import Flask
from flask import url_for
from flask import render_template
from flask import current_app, g
from pathlib import Path
from flask import redirect
from flask import request
import sqlite3

app = Flask(__name__)

app.secret_key = 'b05c5dafc4a00a8b7548d8fb35e45c1a86553f4f233b15f2d211d1deade97df9'


def get_db():
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    return db


if not Path("database.db").exists() :
    get_db().executescript(Path("SCRIPT.sql").read_text())


@app.route("/")
@app.route('/index')
def index():
    return render_template('index.html', title='Accueil - vous êtes connecté', logo='PowerFourFlash', username=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Identifiants incorrects. Réessayez.'
        else:
            return redirect(url_for('index'))
    return render_template('login.html', title='Créer mon compte', error=error)

@app.route('/signup', methods =['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
    return render_template('signup.html', title='Créer mon compte')


@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'


with app.test_request_context():
    print(url_for('profile', username='John Doe'))
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('signup'))
