from flask import Flask, redirect
from flask import url_for
from flask import flash
from flask import session
from flask import render_template
from flask import request

app = Flask(__name__)

app.secret_key = 'b05c5dafc4a00a8b7548d8fb35e45c1a86553f4f233b15f2d211d1deade97df9'


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


@app.route("/")
def index():
    return "Index Page"


@app.route("/test/")
def test():
    return "<p>Test !</p>"


@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'


with app.test_request_context():
    print(url_for('profile', username='John Doe'))
    print(url_for('index'))
