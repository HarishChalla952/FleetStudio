from db import db

class DoctorModel(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(80))
    specilization = db.Column(db.String(80))
    gender = db.Column(db.String(6))

    patients = db.relationship('PatientModel', lazy='dynamic')

    def __init__(self, doctor_name, specilization, gender):        
        self.doctor_name = doctor_name
        self.specilization = specilization
        self.gender = gender.upper()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()     

    def json(self):
        return {'doctor_name': self.doctor_name, 'specilization': self.specilization, 'gender':self.gender} 


    def patients_json(self):
        return {'doctor_name': self.doctor_name, 'patients history': [patient.json() for patient in self.patients.all()]}

 
    @classmethod
    def find_by_name(cls, doctor_name):
        return cls.query.filter_by(doctor_name=doctor_name).first()