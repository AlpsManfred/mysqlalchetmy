from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data import db_session
from data.users import User


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email',
                  'hashed_password', 'created_date'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email',
                  'hashed_password', 'created_date')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User()
        user.surname = args['surname']
        user.name = args['name']
        user.age = args['age']
        user.position = args['position']
        user.speciality = args['speciality']
        user.address = args['address']
        user.email = args['email']
        user.hashed_password = args['hashed_password']

        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True, type=str)
parser.add_argument('name', required=True, type=str)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True, type=str)
parser.add_argument('speciality', required=True, type=str)
parser.add_argument('address', required=True, type=str)
parser.add_argument('email', required=True, type=str)
parser.add_argument('hashed_password', required=True, type=str)