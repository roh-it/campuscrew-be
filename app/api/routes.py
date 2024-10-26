from flask import Blueprint, request, jsonify
from app.models import Users 

api = Blueprint('api', __name__)

@api.route('/createUser', methods=['POST'])
def create_user():
    data = request.get_json()
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    email = data.get('email')
    password = data.get('password')
    if not password or not email:
        return jsonify({'error': 'E-Mail and password are required'}), 400
    new_user, error = Users.create_user(email, password, firstName, lastName)
    if error:
        return jsonify({'error': error}), 500

    return jsonify({'message': 'User created successfully'}), 201


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'E-Mail and password are required'}), 400

    user = Users.query.filter_by(email=email).first()
    
    if user and Users.check_password(user, password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 400