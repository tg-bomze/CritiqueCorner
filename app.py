from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import json
import os
import hashlib
from datetime import datetime, timezone

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

# --- Functions ---

def load_users():
    """Loads user data from the JSON file."""
    if not os.path.exists(USERS_FILE):
        return {} 
    try:
        with open(USERS_FILE, 'r') as f:
            content = f.read()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_users(users):
    """Saves user data to the JSON file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def load_feedback(username):
    """Loads feedback for a specific user."""
    feedback_file = os.path.join(DATA_DIR, f'feedback_{username}.json')
    if not os.path.exists(feedback_file):
        return []
    try:
        with open(feedback_file, 'r') as f:
            content = f.read()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_feedback(username, feedback_list):
    """Saves feedback for a specific user."""
    os.makedirs(DATA_DIR, exist_ok=True)
    feedback_file = os.path.join(DATA_DIR, f'feedback_{username}.json')
    with open(feedback_file, 'w', encoding='utf-8') as f:
        json.dump(feedback_list, f, indent=4, ensure_ascii=False)

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# --- Routes ---

@app.route('/')
def index():
    """Renders the main page."""
    users = load_users()
    registered_usernames = list(users.keys()) 
    
    user_feedback = []
    if 'username' in session:
        user_feedback = load_feedback(session['username'])
        
    return render_template('index.html', 
                           registered_usernames=registered_usernames,
                           user_feedback=user_feedback)

@app.route('/register', methods=['POST'])
def register():
    """Handles user registration."""
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Username and password are required.', 'error')
        return redirect(url_for('index'))

    users = load_users()
    if username in users:
        flash('Username already exists.', 'error')
        return redirect(url_for('index'))

    users[username] = hash_password(password)
    save_users(users)
    
    flash('Registration successful! Please log in.', 'success')
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    """Handles user login."""
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Username and password are required.', 'error')
        return redirect(url_for('index'))

    users = load_users()
    if username not in users or users[username] != hash_password(password):
        flash('Invalid username or password.', 'error')
        return redirect(url_for('index'))

    session['username'] = username 
    flash('Login successful!', 'success')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Logs the user out."""
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    """Handles submission of anonymous feedback."""
    target_username = request.form.get('target_username')
    feedback_text = request.form.get('feedback_text')

    if not target_username or not feedback_text:
        flash('Please select a user and enter feedback.', 'error')
        return redirect(url_for('index'))
        
    users = load_users()
    if target_username not in users:
        flash('Selected user does not exist.', 'error')
        return redirect(url_for('index'))

    feedback_list = load_feedback(target_username)
    utc_now = datetime.now(timezone.utc)

    new_feedback = {
        'date': utc_now.date().isoformat(),
        'text': feedback_text
    }

    feedback_list.insert(0, new_feedback)
    save_feedback(target_username, feedback_list)

    return redirect(url_for('index'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    """Deletes the logged-in user's account and feedback."""
    if 'username' not in session:
        flash('You need to be logged in to delete your account.', 'error')
        return redirect(url_for('index'))

    username_to_delete = session['username']
    
    users = load_users()
    if username_to_delete in users:
        del users[username_to_delete]
        save_users(users)

    feedback_file = os.path.join(DATA_DIR, f'feedback_{username_to_delete}.json')
    if os.path.exists(feedback_file):
        try:
            os.remove(feedback_file)
        except OSError as e:
            flash(f'Error deleting feedback file: {e}', 'error')
            print(f"Error deleting {feedback_file}: {e}")

    session.pop('username', None)
    flash('Your account has been successfully deleted.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(USERS_FILE):
        save_users({})
    app.run(debug=False)
