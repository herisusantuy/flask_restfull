import sqlite3
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help='This field cannot be blank.')
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help='This field cannot be blank.')


class UserRegister(Resource):
    _user_parser.add_argument('full_name',
                              type=str,
                              required=False,
                              help='This field cannot be blank.')
    _user_parser.add_argument('address',
                              type=str,
                              required=False,
                              help='This field cannot be blank.')
    _user_parser.add_argument('phone',
                              type=str,
                              required=False,
                              help='This field cannot be blank.')
    _user_parser.add_argument('email',
                              type=str,
                              required=False,
                              help='This field cannot be blank.')
    _user_parser.add_argument('is_driver',
                              type=str,
                              required=False,
                              help='This field cannot be blank.')

    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created succesfully.'}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found.'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found.'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # _user_parser = reqparse.RequestParser()
        data = _user_parser.parse_args()
        print(data, 'DATA')
        user = UserModel.find_by_username(data['username'])
        # this is what the 'auntheticate()' funtion used to do
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                # 'refresh_token': refresh_token,
                'username': user.username,
                'role': user.is_driver
            }
        else:
            return {'message': 'Invalid credentials'}, 401
