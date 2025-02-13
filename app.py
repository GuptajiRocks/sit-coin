from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import qrcode
from dotenv import load_dotenv
from psycopg2 import pool, sql

load_dotenv()

app = Flask(__name__)
app.secret_key = '123'

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
    connection_string = os.getenv('DATABASE_URL')
    connection_pool = pool.SimpleConnectionPool(1, 10, connection_string)
    conn = connection_pool.getconn()
    return conn

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        phone = request.form['phone']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, phone, password, balance) VALUES (%s, %s, %s, %s)',(username, phone, password, 1000))
            conn.commit()
            #user_id = cursor.execute('SELECT id FROM users WHERE username = %s', (username,)).fetchone()['id']
        finally:
            conn.close()

        qr_data = f"user_id:{str(phone)}"
        qr = qrcode.make(qr_data)
        qr_path = f'static/qr_codes/{phone}.png'
        os.makedirs(os.path.dirname(qr_path), exist_ok=True)
        qr.save(qr_path)

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        phone = str(phone)
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE phone = %s', (phone,))
        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid phone or password.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access your dashboard.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    conn.close()

    qr_path = f'static/qr_codes/{user_id}.png'
    return render_template('dashboard.html', user=user, qr_path=qr_path)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)