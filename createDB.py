import sqlite3

conn = sqlite3.connect('fleet.db') # opens connection and creates db if it doesn't exist
print("Database opened")

c = conn.cursor()

#create users table
c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT(80) NOT NULL,password TEXT(80) NOT NULL, role TEXT(40))')
#create doctors table
c.execute('CREATE TABLE IF NOT EXISTS doctors(id INTEGER PRIMARY KEY AUTOINCREMENT,doctor_name VARCHAR(80) NOT NULL,specilization VARCHAR(80), gender VARCHAR(6))')
#create patients table
c.execute('CREATE TABLE IF NOT EXISTS patients(patient_id INTEGER  PRIMARY KEY AUTOINCREMENT, patient_name VARCHAR(80) NOT NULL, doctor_id INTEGER, gender VARCHAR(6),symptoms varchar(255),disease varchar(256),prescription VARCHAR(256), suggestion VARCHAR(256),FOREIGN KEY(doctor_id) REFERENCES doctors(id))')

print("successfully created")

conn.commit()
conn.close()