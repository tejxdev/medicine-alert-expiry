from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime, timedelta
from config import db_config

app = Flask(__name__)

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)

@app.route('/')
def index():
    today = datetime.today()
    warning_date = today + timedelta(days=30)

    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()

    for med in medicines:
        expiry = med['expiry_date']
        if expiry < today.date():
            med['status'] = 'Expired'
        elif expiry <= warning_date.date():
            med['status'] = 'Expiring Soon'
        else:
            med['status'] = 'Safe'

    return render_template('index.html', medicines=medicines)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    expiry = request.form['expiry']
    quantity = request.form['quantity']

    cursor.execute("INSERT INTO medicines (name, expiry_date, quantity) VALUES (%s, %s, %s)", (name, expiry, quantity))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
