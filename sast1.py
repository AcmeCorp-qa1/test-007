from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, make_response
import sqlite3
import os
import subprocess
import pickle
import hashlib
import random
import requests
import xml.etree.ElementTree as ET
from urllib.parse import unquote

app = Flask(__name__)

# --- Hardcoded secrets (CWE-798) ---
app.secret_key = 'vulnerable_secret_key'
DB_PASSWORD = "SuperSecretDBPass123!"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
# ghp_abc123def456ghi789jkl012mno345pqr678

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Insecure CORS (CWE-942) ---
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT, content TEXT)''')
    conn.close()


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# --- Weak password hashing (CWE-327 / CWE-916) ---
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


# --- Insecure token generation using non-cryptographic PRNG (CWE-338) ---
def generate_reset_token():
    return str(random.randint(100000, 999999))


# Homepage
@app.route('/')
def home():
    return render_template('index.html')


# Vulnerable Login - SQL Injection
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        user = conn.execute(query).fetchone()
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')


# --- Registration with weak hashing + SQL injection ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = hash_password(password)  # MD5, no salt
        conn = get_db_connection()
        conn.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{hashed}')")
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')


# Vulnerable Dashboard with IDOR and XSS
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    conn = get_db_connection()
    posts = conn.execute(f"SELECT * FROM posts WHERE user_id = {user_id}").fetchall()  # IDOR vulnerability
    return render_template('dashboard.html', posts=posts)


# ghp_abc123def456ghi789jkl012mno345pqr678
# Create post - vulnerable to XSS
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = session['user_id']
        conn = get_db_connection()
        conn.execute("INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)", (user_id, title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('create_post.html')


# Unvalidated file upload - vulnerable to malicious files + path traversal (CWE-434 / CWE-22)
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename  # no sanitization, no extension whitelist
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f"File uploaded: {filename}"
    return render_template('upload.html')


# --- Path traversal via user-controlled filename (CWE-22) ---
@app.route('/download/<path:filename>')
def download_file(filename):
    filename = unquote(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# --- Command injection (CWE-78) ---
@app.route('/ping', methods=['GET', 'POST'])
def ping_host():
    if request.method == 'POST':
        host = request.form['host']
        result = os.popen(f"ping -c 1 {host}").read()
        return f"<pre>{result}</pre>"
    return render_template('ping.html')


@app.route('/convert', methods=['POST'])
def convert_file():
    input_file = request.form['input_file']
    output_file = request.form['output_file']
    # Shell injection via subprocess with shell=True and unsanitized input
    subprocess.call(f"convert {input_file} {output_file}", shell=True)
    return "Conversion complete"


# --- Insecure deserialization (CWE-502) ---
@app.route('/load_profile', methods=['POST'])
def load_profile():
    data = request.form['profile_data']
    profile = pickle.loads(data.encode('latin1'))  # untrusted pickle input
    return f"Loaded profile for {profile}"


# --- Use of eval() on user input (CWE-95) ---
@app.route('/calculate', methods=['POST'])
def calculate():
    expression = request.form['expression']
    result = eval(expression)
    return f"Result: {result}"


# --- SSRF (CWE-918) ---
@app.route('/fetch_url', methods=['POST'])
def fetch_url():
    target_url = request.form['url']
    response = requests.get(target_url)
    return response.text


# --- XXE via external entity expansion (CWE-611) ---
@app.route('/parse_xml', methods=['POST'])
def parse_xml():
    xml_data = request.data
    parser = ET.XMLParser()
    root = ET.fromstring(xml_data, parser=parser)
    return f"Parsed root tag: {root.tag}"


# --- Open redirect (CWE-601) ---
@app.route('/redirect')
def open_redirect():
    next_url = request.args.get('next')
    return redirect(next_url)


# --- Sensitive data exposure via logging (CWE-532) ---
@app.route('/debug_login', methods=['POST'])
def debug_login():
    username = request.form['username']
    password = request.form['password']
    print(f"Login attempt: username={username}, password={password}")  # credentials in logs
    return "Logged"


# --- Missing authentication on sensitive admin action (CWE-306) ---
@app.route('/admin/delete_user/<int:user_id>')
def delete_user(user_id):
    conn = get_db_connection()
    conn.execute(f"DELETE FROM users WHERE id = {user_id}")  # no auth check + SQLi
    conn.commit()
    conn.close()
    return f"User {user_id} deleted"


# --- Insecure cookie configuration (CWE-614 / CWE-1004) ---
@app.route('/set_pref')
def set_pref():
    resp = make_response("Preference set")
    resp.set_cookie('theme', 'dark', secure=False, httponly=False)
    return resp


# email@gmail.com
# Insecure Direct Object Reference (IDOR)
@app.route('/view_post/<int:post_id>')
def view_post(post_id):
    conn = get_db_connection()
    post = conn.execute(f"SELECT * FROM posts WHERE id = {post_id}").fetchone()  # IDOR vulnerability
    if post:
        return render_template('view_post.html', post=post)
    return "Post not found", 404


if __name__ == '__main__':
    init_db()
    # Debug mode enabled in what looks like production entrypoint (CWE-489)
    app.run(debug=True, host='0.0.0.0')
