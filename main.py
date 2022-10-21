from flask import Flask
from flask import url_for
from flask import flash
from flask import session
from flask import render_template

app = Flask(__name__)

app.secret_key = 'b05c5dafc4a00a8b7548d8fb35e45c1a86553f4f233b15f2d211d1deade97df9'


def calculate_power_four_grid(table, chosen_column, playing_player_number):
    playing_player_mark = "X" if playing_player_number == 1 else "O"
    if 6 >= chosen_column >= 0:
        for line in table:
            if line[chosen_column] == ".":
                line[chosen_column] = playing_player_mark
                break
        else:
            flash("The chosen column is full")
    else:
        flash("Pick a number between 0 and 6 please")


@app.route("/power_four")
def power_four():
    if 'grid' in session:
        calculate_power_four_grid(session['grid'], 5, 1)

        # We are storing our grid in session, and we modify a list in a dictionary so the session doesn't see that
        # the session variable has been changed, so we need to 'force' update it
        session['grid'] = session['grid']

        return render_template('power_four.html', grid=session['grid'])
    else:
        session['grid'] = [["."] * 7 for i in range(6)]
        return render_template('power_four.html', grid=session['grid'])



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
