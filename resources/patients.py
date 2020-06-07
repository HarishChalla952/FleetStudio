from flask_restful import Resource, reqparse
from models.patients import PatientModel
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    get_jwt_claims
)

class Patient(Resource):

    patient_parser = reqparse.RequestParser()
    patient_parser.add_argument('doctor_id', type=str, required=False, help="This field refers to doctor_id")
    patient_parser.add_argument('gender', type=str, required=True, help="This field cannot be blank.")
    patient_parser.add_argument('symptoms', type=str, required=True, help="This field explains symptoms")
    patient_parser.add_argument('disease', type=str, required=False, help="This field explains disease")
    patient_parser.add_argument('prescription', type=str, required=False, help="This field gives details of prescription")
    patient_parser.add_argument('suggestion', type=str, required=False, help="This field gives details of suggestions")

    @jwt_required
    def post(self, patient_name):
        claims = get_jwt_claims()
        if claims['role'] == "PATIENT" :
            data = Patient.patient_parser.parse_args()

            patient_details = PatientModel(patient_name, data['doctor_id'], data['gender'],data['symptoms'],\
                              data['disease'], data['prescription'], data['suggestion'])
            try:            
                patient_details.save_to_db()
            except Exception as e:
                return{"message": "Unable to insert patient {} data due to error {}". format(patient_name, e)}

            return patient_details.json()
        return {"message" : "Only Patients can post the details"}



class MedicinesHistory(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        user_id = get_jwt_identity()
        if claims['role'] == "PATIENT" :
            medicinesHistory = [patient.json() for patient in PatientModel.query.filter_by(patient_id=user_id)]
            return {"Medicines history" : medicinesHistory}, 200
        else:
            return {"message" : "Only Patients can view the medicines history "}, 401
