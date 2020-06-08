from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, UserLogin, UserLogout
from resources.doctors import Doctor, PatientsHistory, MedicineRespond, HealthSuggestion
from resources.patients import Patient,MedicinesHistory
from models.user import UserModel


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fleet.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'somerandomthingshere'

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    user_details=UserModel.find_by_userid(identity)
    print("this is user role  add claims to jwt {}".format(user_details['role']))
    return {'role': user_details['role'], 'username':user_details['username'], 'id':user_details['id']}


api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Doctor, '/doctor')
api.add_resource(PatientsHistory, '/patientHistory')
api.add_resource(Patient, '/medicineSuggestion')
api.add_resource(MedicinesHistory, '/medicinesHistory')
api.add_resource(MedicineRespond, '/medicinesRespond/<string:patientName>')
api.add_resource(HealthSuggestion, '/healthSuggestion/<string:patientName>')




if __name__ == '__main__':
    from db import db
    
    db.init_app(app)

    app.run(port=5000, debug=True)