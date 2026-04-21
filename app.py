from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",  # change on each laptop
    database="hospital_db"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_patient():
    name = request.form['name']
    age = request.form['age']

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO patients (name, age) VALUES (%s, %s)",
        (name, age)
    )
    db.commit()

    return redirect('/view')

@app.route('/view')
def view():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()
    return render_template('view.html', patients=data)

@app.route('/delete/<int:id>')
def delete(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM patients WHERE patient_id=%s", (id,))
    db.commit()
    return redirect('/view')

if __name__ == '__main__':
    app.run(debug=True)