import json
from flask import Flask, render_template, request, redirect, url_for
import threading
import subprocess

app = Flask(__name__)

USER_DATA_FILE = 'users.json'

def load_users():
    try:
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_users(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)

users = load_users()

def run_game():
    subprocess.run(["python3", "breaker_game.py"])

def start_game_in_thread():
    game_thread = threading.Thread(target=run_game)
    game_thread.daemon = True
    game_thread.start()

@app.route('/')
def register():
    return render_template('register.html')

@app.route('/submit_registration', methods=['POST'])
def submit_registration():
    name = request.form['name']
    email = request.form['email']
    users.append({'name': name, 'email': email})
    save_users(users)
    return redirect(url_for('game_page'))

@app.route('/game')
def game_page():
    return render_template('game.html')

@app.route('/start_game')
def start_game():
    start_game_in_thread()
    return "Game Started!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
