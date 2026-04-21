from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Hidden@7",  # put your MySQL password
    database="hospital_db"
)

# ================= PATIENTS =================

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()
    return render_template('index.html', patients=data)

@app.route('/add', methods=['POST'])
def add_patient():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    issue = request.form['health_issue']

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO patients (name, age, gender, health_issue) VALUES (%s, %s, %s, %s)",
        (name, age, gender, issue)
    )
    db.commit()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete_patient(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM patients WHERE patient_id=%s", (id,))
    db.commit()
    return redirect('/')

# ================= DOCTORS =================

@app.route('/doctors')
def doctors():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM doctors")
    data = cursor.fetchall()
    return render_template('doctors.html', doctors=data)

@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    name = request.form['name']
    specialization = request.form['specialization']

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO doctors (name, specialization) VALUES (%s, %s)",
        (name, specialization)
    )
    db.commit()

    return redirect('/doctors')  # ✅ stay on doctors page

@app.route('/delete_doctor/<int:id>')
def delete_doctor(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM doctors WHERE doctor_id=%s", (id,))
    db.commit()
    return redirect('/doctors')

# ================= RUN APP =================

if __name__ == '__main__':
    app.run(debug=True)