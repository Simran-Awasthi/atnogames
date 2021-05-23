from flask import Flask, render_template
import json, os

app = Flask(__name__, template_folder='./templates/', static_folder='./static/')

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/games')
def get_games():
    with open('game_info.json', 'r') as f:
        data = json.load(f)
    return render_template('games_view.html', games=data['games_list'])


if __name__ == '__main__':
    app.run()