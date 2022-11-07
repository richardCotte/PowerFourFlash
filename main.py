from turtle import title
from flask import Flask
from flask import url_for
from flask import render_template
from flask import redirect
from flask import request
import sqlite3
import models as dbHandler

app = Flask(__name__)

app.secret_key = 'b05c5dafc4a00a8b7548d8fb35e45c1a86553f4f233b15f2d211d1deade97df9'


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Accueil - vous êtes connecté', logo='PowerFourFlash')


@app.route('/login', methods=['GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['email'] != 'admin' or request.form['pswd'] != 'admin':
            error = 'Identifiants incorrects. Réessayez.'
        else:
            return redirect(url_for('index'))
    return render_template('login.html', title='Se connecter', error=error)

@app.route('/signup', methods =['POST', 'GET'])
def signup():
    if request.method=='POST':
        nickname = request.form['nickname']
   	    email = request.form['email']
   	    pswd = request.form['pswd']
   		dbHandler.insertUser(email, nickname, pswd)
   		users = dbHandler.retrieveUsers()
        return render_template('signup.html', title='Créer mon compte', users=users)
    else:
        return render_template('login.html')



@app.route('/user/<username>')
def profile(nickname):
    return f'{nickname}\'s profile'

with app.test_request_context():
    #print(url_for('', username='John Doe'))
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('signup'))
