from flask import Blueprint, request, jsonify
from db import mongo
import json
from werkzeug.security import generate_password_hash

register_bp = Blueprint("register",__name__)

@register_bp.route("/", methods=["POST"])
def create_user():
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

