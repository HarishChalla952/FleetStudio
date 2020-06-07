from db import db

class PatientModel(db.Model):
    __tablename__ = 'patients'

    patient_id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(80))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    gender = db.Column(db.String(6))
    symptoms = db.Column(db.String(256))
    disease = db.Column(db.String(256))
    prescription = db.Column(db.String(256))
    suggestion = db.Column(db.String(256))

    doctor = db.relationship('DoctorModel')

    def __init__(self, patient_name, doctor_id, gender,symptoms, disease, prescription,suggestion):
        self.patient_name = patient_name
        self.doctor_id = doctor_id
        self.gender = gender.upper()
        self.symptoms = symptoms
        self.disease = disease
        self.prescription = prescription
        self.suggestion = suggestion


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()     

    def json(self):
        return {'patient_name': self.patient_name, 'doctor_id': self.doctor_id, 'gender':self.gender, \
             'symptoms': self.symptoms, 'disease':self.disease, 'prescription':self.prescription, 'suggestion':self.suggestion}

    @classmethod
    def find_patient(cls, patientName):
        patient = (cls.query.filter_by(patient_name=patientName).first())
        return patient
