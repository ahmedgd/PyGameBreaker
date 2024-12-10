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
    try:
        # محاولة تشغيل ملف اللعبة عبر subprocess
        subprocess.run(["python3", "breaker_game.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running game: {e}")
        return f"An error occurred while starting the game: {e}"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return f"An unexpected error occurred: {e}"

def start_game_in_thread():
    # لا نحتاج لارجاع أي شيء هنا، فقط تشغيل اللعبة في خيط مستقل
    game_thread = threading.Thread(target=run_game)
    game_thread.daemon = True  # تأكد من أن الخيط سيغلق تلقائيًا عند إنهاء التطبيق
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
    start_game_in_thread()  # تشغيل اللعبة في خيط خلفي
    return "Game Started!"  # إرجاع رسالة تأكيد بأن اللعبة قد بدأت

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
