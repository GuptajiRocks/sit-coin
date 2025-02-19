from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import os
import qrcode
from dotenv import load_dotenv
import psycopg2
import io

load_dotenv()

app = Flask(__name__)
app.secret_key = '123'

@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/adlogin")
def admin_entry():
    return render_template("adlogin.html")

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

@app.route("/admin/details")
def user_details():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, phone, balance FROM users;")
    rst = cursor.fetchall()

    return render_template("addet.html", users=rst)

def get_db_connection():
    connection_string = os.getenv('DATABASE_URL')
    connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, connection_string)
    conn = connection_pool.getconn()
    return conn

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        phone = request.form['phone']
        password = generate_password_hash(request.form['password'])

        qr_data = f"user_id:{str(phone)}"
        qr = qrcode.make(qr_data)
        qr_io = io.BytesIO()
        qr.save(qr_io, format="PNG")
        qr_binary = qr_io.getvalue()

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, phone, password, balance, qr_code) VALUES (%s, %s, %s, %s, %s)',(username, phone, password, 1000, psycopg2.Binary(qr_binary)))
            conn.commit()
        finally:
            conn.close()        

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

    cursor.execute('SELECT sender_phone, receiver_phone, amount, timestamp FROM transactions WHERE sender_phone = %s or receiver_phone = %s ORDER BY timestamp DESC',
                   (user[2], user[2],))
    transactions = cursor.fetchall()

    conn.close()
    return render_template('dashboard.html', user=user, transactions=transactions)

@app.route('/send_money', methods=['POST'])
def send_money():
    sender_phone = request.form.get('sender_phone')
    receiver_phone = request.form.get('receiver_phone')
    amount = request.form.get('amount')

    if not sender_phone or not receiver_phone or not amount:
        flash("All fields are required!", "danger")
        return redirect(url_for('dashboard'))

    try:
        amount = float(amount)
        if amount <= 0:
            flash("Amount must be greater than zero!", "danger")
            return redirect(url_for('dashboard'))
    except ValueError:
        flash("Invalid amount! Please enter a valid number.", "danger")
        return redirect(url_for('dashboard'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, balance FROM users WHERE phone = %s", (sender_phone,))
    sender = cursor.fetchone()

    if not sender:
        flash("Sender not found!", "danger")
        conn.close()
        return redirect(url_for('dashboard'))

    sender_id, sender_balance = sender

    cursor.execute("SELECT id FROM users WHERE phone = %s", (receiver_phone,))
    receiver = cursor.fetchone()

    if not receiver:
        flash("Receiver not found!", "danger")
        conn.close()
        return redirect(url_for('dashboard'))

    receiver_id = receiver[0]

    if sender_balance < amount:
        flash("Insufficient balance!", "danger")
        conn.close()
        return redirect(url_for('dashboard'))

    cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (amount, sender_id))
    cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, receiver_id))

    cursor.execute("INSERT INTO transactions (sender_phone, receiver_phone, amount) VALUES (%s, %s, %s)",
                   (sender_phone, receiver_phone, amount))

    conn.commit()
    conn.close()

    flash(f"₹{amount} sent successfully to {receiver_phone}!", "success")
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)