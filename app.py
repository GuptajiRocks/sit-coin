from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import qrcode

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/signup")
def sign_up():
    return render_template("signup.html")

@app.route("/contact")
def contact_page():
    return render_template("contact.html")

@app.route("/aboutus")
def about_us_page():
    return render_template("aboutus.html")

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['phone']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        try:
            conn.execute(
                'INSERT INTO users (username, email, password, balance) VALUES (?, ?, ?, ?)',
                (username, email, password, 1000)
            )
            conn.commit()
            user_id = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()['id']
        finally:
            conn.close()

        # Generate QR code
        qr_data = f"user_id:{user_id}"
        qr = qrcode.make(qr_data)
        qr_path = f'static/qr_codes/{user_id}.png'
        os.makedirs(os.path.dirname(qr_path), exist_ok=True)
        qr.save(qr_path)

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')