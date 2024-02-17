from flask import Blueprint, request, jsonify
from db import mongo
import json
from werkzeug.security import generate_password_hash, check_password_hash

register_bp = Blueprint("register",__name__)

@register_bp.route("/", methods=["POST"])
def register_user():
    try:
        registration_data = request.json
        first_name = registration_data.get('first_name')
        last_name = registration_data.get('last_name')
        email = registration_data.get('email')
        password = registration_data.get('password')
        confirm_password = registration_data.get('confirm_password')
        if not all([first_name, last_name, email, password, confirm_password]):
            return jsonify({'error': 'All fields are required.'}), 400

        if password != confirm_password:
            return jsonify({'error': 'Passwords do not match.'}), 400

        # Check if email is already registered
        if mongo.db.Customers.find_one({'email': email}):
            return jsonify({'error': 'Email already registered.'}), 400
        
        hashed_password = generate_password_hash(password)
        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': hashed_password
        }   
        mongo.db.Customers.insert_one(user_data)
        return jsonify({'message': 'Registration successful.'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500  
    

login_bp = Blueprint("login",__name__)

@login_bp.route("/", methods=["GET"])
def login_user_valid():
    try:
        login_data = request.json
        email = login_data.get('email')
        password = login_data.get('password')
        userData = {}

        if any([not email, not password]):
            return jsonify({'error': 'Email and password are required.'}), 400

        user = mongo.db.Customers.find_one({'email': email})

        if not user:
            return jsonify({'error': 'User not found.'}), 404

        if not check_password_hash(user['password'], password):
            return jsonify({'error': 'Incorrect password.'}), 401
    
        userData['_id'] = str(user['_id'])
        userData['first_name'] = user['first_name']
        userData['last_name'] = user['last_name']
        userData['email'] = user['email']
        return jsonify({'message': 'Login successful.', 'user': userData}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
