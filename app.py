from flask import Flask, jsonify, render_template, request
import sqlite3
import os

app = Flask(__name__, static_folder="frontend", template_folder="frontend")

def get_db_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "database", "hospital_management.db")

def create_database_if_not_exists():
    """Create the database if it doesn't exist"""
    db_path = get_db_path()
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}, creating it now...")
       
        from create_database import create_database
        create_database()
        print("Database created successfully!")
    else:
        print(f"Database already exists at {db_path}")

def get_data(query, params=()):
    try:
        conn = sqlite3.connect(get_db_path())
        conn.row_factory = sqlite3.Row  
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def execute_query(query, params=()):
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return True, last_id
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False, str(e)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/add')
def add_data_page():
    return render_template("add_data.html")

@app.route('/api/patients')
def patients():
    rows = get_data("SELECT * FROM patients")
    print(f"Retrieved {len(rows)} patients from database")
    return jsonify(rows)

@app.route('/api/doctors')
def doctors():
    rows = get_data("SELECT * FROM doctors")
    print(f"Retrieved {len(rows)} doctors from database")
    return jsonify(rows)

@app.route('/api/appointments')
def appointments():
    rows = get_data("SELECT * FROM appointments")
    print(f"Retrieved {len(rows)} appointments from database")
    return jsonify(rows)

@app.route('/api/add_patient', methods=['POST'])
def add_patient():
    data = request.json
    query = "INSERT INTO patients (patient_id, name, age, gender, phone) VALUES (?, ?, ?, ?, ?)"
    params = (
        data.get('patient_id'),
        data.get('name'),
        data.get('age'),
        data.get('gender'),
        data.get('phone')
    )
    success, result = execute_query(query, params)
    if success:
        return jsonify({"status": "success", "message": "Patient added successfully"}), 201
    else:
        return jsonify({"status": "error", "message": f"Failed to add patient: {result}"}), 500

@app.route('/api/add_doctor', methods=['POST'])
def add_doctor():
    data = request.json
    query = "INSERT INTO doctors (doctor_id, name, specialty, phone) VALUES (?, ?, ?, ?)"
    params = (
        data.get('doctor_id'),
        data.get('name'),
        data.get('specialty'),
        data.get('phone')
    )
    success, result = execute_query(query, params)
    if success:
        return jsonify({"status": "success", "message": "Doctor added successfully"}), 201
    else:
        return jsonify({"status": "error", "message": f"Failed to add doctor: {result}"}), 500

@app.route('/api/add_appointment', methods=['POST'])
def add_appointment():
    data = request.json
   
    query = "INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date) VALUES (?, ?, ?, ?)"
    params = (
        data.get('appointment_id'),
        data.get('patient_id'),
        data.get('doctor_id'),
        data.get('appointment_date')  
    )
    success, result = execute_query(query, params)
    if success:
        return jsonify({"status": "success", "message": "Appointment added successfully"}), 201
    else:
        return jsonify({"status": "error", "message": f"Failed to add appointment: {result}"}), 500

if __name__ == '__main__':
    
    create_database_if_not_exists()
    app.run(debug=True)