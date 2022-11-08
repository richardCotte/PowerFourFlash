from importlib.resources import path
from flask import Flask, redirect
from flask import url_for
from flask import flash
from flask import session
from flask import render_template
from flask import request
from flask import current_app, g
from pathlib import Path
from flask import redirect
from flask import request
import sqlite3


app = Flask(__name__)

app.secret_key = "b05c5dafc4a00a8b7548d8fb35e45c1a86553f4f233b15f2d211d1deade97df9"


def get_db():
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    return db


if not Path("database.db").exists():
    get_db().executescript(Path("SCRIPT.sql").read_text())


@app.route("/sinup_player", methods=["POST", "GET"])
def sinup_player():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    if len(username) > 0 and len(email) > 0 and len(password) > 0:
        db = get_db()
        cur = db.cursor()
        sqlRequest = (
            "INSERT INTO player (email, pseudo, pass) VALUES ('%s', '%s', '%s')"
            % (str(email), str(username), str(password))
        )
        cur.execute(sqlRequest)
        db.commit()
        return redirect(url_for("login"))
    else:
        return redirect(url_for("error"))


@app.route("/login_player", methods=["POST", "GET"])
def login_player():
    email = request.form["email"]
    password = request.form["password"]
    if len(email) > 0 and len(password) > 0:
        db = get_db()
        cur = db.cursor()
        sqlRequest = "SELECT * FROM player WHERE email = '%s'" % (str(email))
        cur.execute(sqlRequest)
        rows = cur.fetchall()
        if dict(rows[0])["pass"] == str(password):
            session["email"] = str(email)
            session["username"] = str(dict(rows[0])["pseudo"])
            return redirect(url_for("power_four"))
        else:
            return redirect(url_for("error"))
    else:
        return redirect(url_for("error"))


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


@app.route("/power_four/", methods=["POST", "GET"])
def power_four():
    if "grid" not in session:
        session["grid"] = [["."] * 7 for i in range(6)]
        session["playing_player"] = "X"
    if request.method == "POST":
        chosen_grid = request.form["chosen_grid"]
        if calculate_power_four_grid(
            session["grid"], int(chosen_grid), session["playing_player"]
        ):
            session["playing_player"] = "X" if session["playing_player"] == "O" else "O"

        # We are storing our grid in session, and we modify a list in a dictionary however the session doesn't see that
        # the session variable has been changed, so we need to 'force' update it
        session["grid"] = session["grid"]
        return redirect(url_for("power_four"))

    return render_template(
        "power_four.html",
        grid=session["grid"],
        playing_player=session["playing_player"],
    )


@app.route("/scoreboard")
def scoreboard():
    db = get_db()
    cur = db.cursor()
    sqlRequest = "SELECT p.pseudo, s.win FROM player p INNER JOIN scoreboard s ON p.email = s.emailPlayer ORDER BY s.win DESC"
    cur.execute(sqlRequest)
    rows = cur.fetchall()
    return render_template(
        "scoreboard.html", title="Scoreboard", logo="PowerFourFlash", score=rows
    )


@app.route("/")
@app.route("/index")
def index():
    name = ""
    return render_template(
        "index.html", title="Accueil", logo="PowerFourFlash", username=name
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html", title="Créer mon compte")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html", title="Créer mon compte")


@app.route("/error")
def error():
    return render_template("error.html", title="ERROR")
