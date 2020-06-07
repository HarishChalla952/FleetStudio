from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (create_access_token,create_refresh_token,get_raw_jwt,jwt_required)

from models.user import UserModel
from blacklist import BLACKLIST



class UserRegister(Resource):
    _user_parser = reqparse.RequestParser()
    _user_parser.add_argument('username', type=str, required=True, help="This field cannot be blank.")
    _user_parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")
    _user_parser.add_argument('role', type=str, required=True, help="This field for role of user.")
    def post(self):
        
        data = UserRegister._user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'], data['role'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserLogin(Resource):
    _login_parser = reqparse.RequestParser()
    _login_parser.add_argument('username', type=str, required=True, help="This field cannot be blank.")
    _login_parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")   

    @classmethod
    def post(cls):
        data = UserLogin._login_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        #authentication function
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid Credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']    #jti is "JWT ID" ,a unique identifier for a JWT.
        BLACKLIST.add(jti)
        return {'message': "Logged out successfully"}