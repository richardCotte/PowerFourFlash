from importlib.resources import path
from flask import Flask
from flask import url_for
from flask import render_template
from flask import current_app, g
from pathlib import Path
import sqlite3

app = Flask(__name__)

app.secret_key = 'b05c5dafc4a00a8b7548d8fb35e45c1a86553f4f233b15f2d211d1deade97df9'

if not Path("database.db").exists() :
    get_db().executescript(Path("SCRIPT.sql").read_text())

@app.route("/")
def index():
    return "Index Page"


@app.route("/test/")
def test():
    return "<p>Test !</p>"


@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'


def get_db():
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    return db


with app.test_request_context():
    print(url_for('profile', username='John Doe'))
    print(url_for('index'))
