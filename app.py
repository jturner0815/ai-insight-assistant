from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from logger import log_prompt
from pdf_exporter import export_insight_to_pdf
import sqlite3
import pandas as pd
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = 'supersecretkey'
load_dotenv()

# Configure login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Ensure users.db exists
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )""")
    conn.commit()
    conn.close()

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return User(id=row[0], username=row[1])
    return None

# Groq API settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_groq_api(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route("/")
def home():
    return redirect(url_for("register"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_hash = generate_password_hash(password)
        try:
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
            conn.commit()
            conn.close()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already taken. Choose another.", "danger")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
        row = c.fetchone()
        conn.close()
        if row and check_password_hash(row[1], password):
            user = User(id=row[0], username=username)
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    insight = ""
    if request.method == "POST":
        file = request.files["file"]
        custom_prompt = request.form.get("custom_prompt", "").strip()
        if file:
            df = pd.read_csv(file)
            sample = df.head(10).to_csv(index=False)
            if custom_prompt:
                prompt = (
                    f"Here is a preview of a dataset:\n\n"
                    f"{sample}\n\n"
                    f"User's question: {custom_prompt}"
                )
            else:
                prompt = (
                    f"Here is a preview of a dataset:\n\n"
                    f"{sample}\n\n"
                    f"Please provide 3 clear data-driven insights based on this sample."
                )
            insight = call_groq_api(prompt)
            log_prompt(current_user.username, prompt, insight)
            export_insight_to_pdf(insight, filename='static/insight.pdf')
    return render_template("index.html", insight=insight, username=current_user.username)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
