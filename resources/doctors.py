from flask_restful import Resource, reqparse
from models.doctors import DoctorModel
from models.patients import PatientModel
from flask_jwt_extended import (
    jwt_optional,
    get_jwt_identity,
    jwt_required,
    get_jwt_claims
)


#Doctor Class to post details
class Doctor(Resource):

    doctor_parser = reqparse.RequestParser()
    doctor_parser.add_argument('specilization', type=str, required=True, help="This field cannot be blank.")
    doctor_parser.add_argument('gender', type=str, required=True, help="This field cannot be blank.")    
    #login required and allow user to post only if user is doctor
    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        if claims['role'] == "DOCTOR" :
            if DoctorModel.find_by_name(claims['username']):
                return {'message': "An Doctor with name '{}' already exists.".format(claims['username'])}, 400

            data = Doctor.doctor_parser.parse_args()
            doc_details = DoctorModel(claims['username'], **data, doc_id=claims['id'] )

            try:
                doc_details.save_to_db()
            except Exception as e:
                return {"message" : "Unable to insert doctor {} due to exception {}".format(claims['username'],e)}

            return doc_details.json()

        return {"message" : "Only doctors can post the data"}



#Doctor can get the treated patients history
class PatientsHistory(Resource):
    #check whether loggedin user is doctor
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if claims['role'] == "DOCTOR" :
            patientsHistory = [doctor.patients_json() for doctor in DoctorModel.query.filter_by(doctor_name=claims['username'])]
            return {"patients history" : patientsHistory}, 200
        else:
            return {"message" : "Only Doctors can view the patient history "}, 401


#MedicineRespond class to respond for patients
class MedicineRespond(Resource):
    # check whether the loggedin user is doctor
    @jwt_required
    def post(self, patientName):
        prescription_parser = reqparse.RequestParser()
        prescription_parser.add_argument('disease', type=str, required=True, help="This field cannot be blank.")
        prescription_parser.add_argument('prescription', type=str, required=True, help="This field cannot be blank.")
        data = prescription_parser.parse_args()
        claims = get_jwt_claims()
        user_id = get_jwt_identity()
        if claims['role'] == "DOCTOR" :
            patient = PatientModel.find_patient(patientName)
            #check if the patient has asked for any particular doctor
            if patient and patient.doctor_id==user_id:                
                patient.doctor_id = user_id
                patient.disease= data['disease']
                patient.prescription= data['prescription']
                try:
                    patient.save_to_db()
                except Exception as e:
                    return {"message" : "Unable to insert doctors prescription due to error {}".format(e)}
                return patient.json()
            #If patient doesn't ask for particular doctor any doctor can treat patient
            elif patient and (patient.doctor_id is None):
                patient.doctor_id = user_id
                patient.disease = data['disease']
                patient.prescription= data['prescription']
                try:
                    patient.save_to_db()
                except Exception as e:
                    return {"message" : "Unable to insert doctors prescription due to error {}".format(e)}
                return patient.json()
            #Restrict the doctor if the user asked doctor and loggedin doctor are different
            elif patient and patient.doctor_id != user_id:
                return {"message" : "Only the Doctor {} can treat this patient".format(patient.doctor_id)}
            
            else:            
                return {"message" : "Patient {} doesn't exist.".format(patientName)}
        return {"message" : "Only doctors can give prescriptions."}   



#HealthSuggestion class
class HealthSuggestion(Resource):
    #any loggedin doctor can give suggestion to any patient    
    @jwt_required
    def post(self, patientName):
        suggestion_parser = reqparse.RequestParser()
        suggestion_parser.add_argument('suggestion', type=str, required=True, help="This field cannot be blank.")
        data = suggestion_parser.parse_args()
        claims = get_jwt_claims()
        if claims['role'] == "DOCTOR" :
            patient = PatientModel.find_patient(patientName)
            if patient :                
                patient.suggestion = data['suggestion']
                try:
                    #sug_patient = PatientModel(patient.patient_name, patient.doctor_id, patient.gender, \
                                  #patient.symptoms, patient.disease, patient.prescription,patient.suggestion)
                    patient.save_to_db()
                except Exception as e:
                    return {"message" : "Unable to insert doctors prescription due to error {}".format(e)}
                return patient.json()
            else:
                return {"message" : "patient {} doest not exist".format(patientName)}
        
        return {"message" : "Only doctors can give suggestions"}



