from flask import Blueprint, request, jsonify
from db import mongo
import json
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import Schema, fields

register_bp = Blueprint("register",__name__)

class RegisterSchema(Schema):
    firstName=fields.Str(required=True)
    lastName=fields.Str(required=True)
    email=fields.Str(required=True)
    password=fields.Str(required=True)
    confirmPassword=fields.Str(required=True)

register_schema = RegisterSchema()

@register_bp.route("/", methods=["POST"])
def register_user():
    try:
        registration_data = request.json
        print(registration_data)
        errors = register_schema.validate(registration_data)
        if errors:
            return jsonify({'error': errors,"message":"Missing fields"}), 400
        
        first_name = registration_data.get('firstName')
        last_name = registration_data.get('lastName')
        email = registration_data.get('email')
        password = registration_data.get('password')
        confirm_password = registration_data.get('confirmPassword')
        if not all([first_name, last_name, email, password, confirm_password]):
            return jsonify({"status":"Error",'message': 'All fields are required.'}), 400

        if password != confirm_password:
            return jsonify({"status":"Error",'message': 'Passwords do not match.'}), 400

        print('Checking Email exists')
        # Check if email is already registered
        if mongo.db.Customers.find_one({'email': email}):
            return jsonify({"status":"Error",'message': 'Email already registered.'}), 400
        
        print('Email not exists')
        hashed_password = generate_password_hash(password)
        print('Password has completed')
        user_data = {
            'firstName': first_name,
            'lastName': last_name,
            'email': email,
            'password': hashed_password
        }  
        print('Pushing to Mongo') 
        mongo.db.users.insert_one(user_data)
        print('Pushed to DB')
        return jsonify({'message': 'Registration successful.'}), 200

    except Exception as e:
        return jsonify({"status":"Error",'error': str(e)}), 500  
    

login_bp = Blueprint("login",__name__)

@login_bp.route("/", methods=["GET"])
def login_user_valid():
    try:
        login_data = request.json
        email = login_data.get('email')
        password = login_data.get('password')
        userData = {}

        if any([not email, not password]):
            return jsonify({"status":'Error',"message": 'Email and password are required.'}), 400

        user = mongo.db.users.find_one({'email': email})

        if not user:
            return jsonify({"status":'Error',"message": 'User not found.'}), 404

        if user.get('role', None) and user["role"] == 'admin':
            if user['password'] == password:
                user['_id'] = str(user['_id'])
                return jsonify({"status":"Success","message": 'Login successful.', 'user':user}), 200

        if not check_password_hash(user['password'], password):
            return jsonify({"status":'Error',"message": 'Incorrect password.'}), 401
    
        userData['_id'] = str(user['_id'])
        userData['firstName'] = user['firstName']
        userData['lastName'] = user['lastName']
        userData['email'] = user['email']
        return jsonify({"status":"Success","message": 'Login successful.', 'user': userData}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
