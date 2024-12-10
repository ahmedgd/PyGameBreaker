import json
import logging
from flask import Flask, render_template, request, redirect, url_for
import threading
import subprocess
import os

app = Flask(__name__)

USER_DATA_FILE = 'users.json'

# إعدادات تسجيل الأخطاء
logging.basicConfig(level=logging.DEBUG)

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
    try:
        logging.info("Starting the game...")
        subprocess.run(["python3", "breaker_game.py"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error while running the game: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

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
    port = int(os.environ.get("PORT", 5000))  # تحديد المنفذ من متغير البيئة أو 5000 افتراضيًا
    app.run(debug=True, host="0.0.0.0", port=port)
