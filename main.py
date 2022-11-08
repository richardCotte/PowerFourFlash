import random

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


# This function test if the grid has a winning condition
def check_game_over(grid):
    checked_count_hor = 0
    checked_count_ver = 0
    checked_square_ver = 0
    for i in range(7):
        for line in grid:

            # here the function test if a player won by aligning 4 pieces horizontally
            checked_square_hor = 0
            for square in line:
                if square == checked_square_hor and square != ".":
                    checked_count_hor += 1
                else:
                    checked_count_hor = 0
                if checked_count_hor == 3:
                    return checked_square_hor
                checked_square_hor = square

            # here the function test if a player won by aligning 4 pieces vertically
            if checked_square_ver == line[i] and line[i] != ".":
                checked_count_ver += 1
            else:
                checked_count_ver = 0
            if checked_count_ver == 3:
                return checked_square_ver
            checked_square_ver = line[i]

    for y in range(3):

        # here the function test if a player won by aligning 4 pieces diagonally from bottom left to top right
        for i in range(4):
            checked_count_diag = 0
            checked_square_diag = 0
            for j in range(4):
                if checked_square_diag == grid[j + y][j + i] and grid[j + y][j + i] != ".":
                    checked_count_diag += 1
                else:
                    checked_count_diag = 0
                if checked_count_diag == 3:
                    return checked_square_diag
                checked_square_diag = grid[j + y][j + i]

        # here the function test if a player won by aligning 4 pieces diagonally from bottom right to top left
        for i in range(6, 2, -1):
            checked_count_diag = 0
            checked_square_diag = 0
            for j in range(4):
                if checked_square_diag == grid[j + y][i - j] and grid[j + y][i - j] != ".":
                    checked_count_diag += 1
                else:
                    checked_count_diag = 0
                if checked_count_diag == 3:
                    return checked_square_diag
                checked_square_diag = grid[j + y][i - j]
    return 0


@app.route("/power_four/", methods=['POST', 'GET'])
def power_four():
    if 'grid' not in session:
        session['grid'] = [["."] * 7 for i in range(6)]
        session['playing_player'] = 1
    if request.method == 'POST':
        chosen_grid = request.form['chosen_grid'] if session['playing_player'] == 1 else random.randint(0, 6)
        if calculate_power_four_grid(session['grid'], int(chosen_grid), session['playing_player']):
            session['playing_player'] = 1 if session['playing_player'] == 2 else 2

        # We are storing our grid in session, and we modify a list in a dictionary however the session doesn't see that
        # the session variable has been changed, so we need to 'force' update it
        session['grid'] = session['grid']
        return redirect(url_for('power_four'))

    winner = check_game_over(session['grid'])
    return render_template('power_four.html', grid=session['grid'], playing_player=session['playing_player'],
                           winner=winner)


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
