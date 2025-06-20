
CREATE TABLE patients (
  patient_id NUMBER PRIMARY KEY,
  name VARCHAR2(50),
  age NUMBER,
  gender VARCHAR2(10),
  phone VARCHAR2(15)
);


INSERT INTO patients VALUES (1, 'Ravi Kumar', 30, 'Male', '9999988888');
INSERT INTO patients VALUES (2, 'Sneha Raj', 26, 'Female', '9999933333');


SELECT * FROM patients;



CREATE TABLE doctors (
  doctor_id NUMBER PRIMARY KEY,
  name VARCHAR2(50),
  specialty VARCHAR2(50),
  phone VARCHAR2(15)
);


INSERT INTO doctors VALUES (1, 'Dr. Arjun', 'Cardiologist', '9888877777');
INSERT INTO doctors VALUES (2, 'Dr. Anjali', 'Neurologist', '9888844444');


SELECT * FROM doctors;



CREATE TABLE appointments (
  appointment_id NUMBER PRIMARY KEY,
  patient_id NUMBER,
  doctor_id NUMBER,
  appointment_date DATE,
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
  FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);


INSERT INTO appointments VALUES (1, 1, 1, '2025-05-11');
INSERT INTO appointments VALUES (2, 2, 2, '2025-05-12');


SELECT * FROM appointments;
