import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Vulnerable SQLite database connection
def get_db_connection():
    conn = sqlite3.connect('vulnerable.db')
    return conn

# SQL Injection vulnerability
@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    conn = get_db_connection()
    cursor = conn.cursor()
    # Vulnerable to SQL Injection
    cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')
    user = cursor.fetchone()
    conn.close()
    return jsonify(user)

# Command Injection vulnerability
@app.route('/execute', methods=['POST'])
def execute_command():
    command = request.form['command']
    # Vulnerable to Command Injection
    os.system(command)
    return 'Command executed'

# Insecure Direct Object Reference (IDOR)
@app.route('/profile/<user_id>', methods=['GET'])
def get_profile(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM profiles WHERE user_id = ?', (user_id,))
    profile = cursor.fetchone()
    conn.close()
    return jsonify(profile)

# Insecure Password Storage
@app.route('/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    conn = get_db_connection()
    cursor = conn.cursor()
    # Storing passwords in plain text (insecure)
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()
    return 'User  registered'

if __name__ == '__main__':
    app.run(debug=True)
