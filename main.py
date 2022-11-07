<<<<<<< HEAD
from importlib.resources import path
from flask import Flask
=======
from flask import Flask, redirect
>>>>>>> origin/powerFourBack
from flask import url_for
from flask import flash
from flask import session
from flask import render_template
<<<<<<< HEAD
from flask import current_app, g
from pathlib import Path
from flask import redirect
from flask import request
import sqlite3
=======
from flask import request
>>>>>>> origin/powerFourBack

app = Flask(__name__)

app.secret_key = 'b05c5dafc4a00a8b7548d8fb35e45c1a86553f4f233b15f2d211d1deade97df9'


<<<<<<< HEAD
def get_db():
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    return db


if not Path("database.db").exists() :
    get_db().executescript(Path("SCRIPT.sql").read_text())
=======
def calculate_power_four_grid(table, chosen_column, playing_player):
    if 6 >= chosen_column >= 0:
        for line in table:
            if line[chosen_column] == ".":
                line[chosen_column] = playing_player
                return True
        flash("The chosen column is full")
        return False
    else:
        flash("The chosen column must be between 0 and 6")
        return False


@app.route("/power_four/", methods=['POST', 'GET'])
def power_four():
    if 'grid' not in session:
        session['grid'] = [["."] * 7 for i in range(6)]
        session['playing_player'] = "X"
    if request.method == 'POST':
        chosen_grid = request.form['chosen_grid']
        if calculate_power_four_grid(session['grid'], int(chosen_grid), session['playing_player']):
            session['playing_player'] = "X" if session['playing_player'] == "O" else "O"

        # We are storing our grid in session, and we modify a list in a dictionary however the session doesn't see that
        # the session variable has been changed, so we need to 'force' update it
        session['grid'] = session['grid']
        return redirect(url_for('power_four'))

    return render_template('power_four.html', grid=session['grid'], playing_player=session['playing_player'])
>>>>>>> origin/powerFourBack


@app.route("/")
@app.route('/index')
def index():
    name =""
    return render_template('index.html', title='Accueil - vous êtes connecté', logo='PowerFourFlash', username=name)

@app.route('/login', methods=['POST'])
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
