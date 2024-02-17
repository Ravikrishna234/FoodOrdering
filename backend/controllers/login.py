from flask import Blueprint, request, jsonify
from db import mongo
import json
from werkzeug.security import check_password_hash

login_bp = Blueprint("login",__name__)

@login_bp.route("/", methods=["POST"])
def login_user_valid():
    try:
        login_data = request.json
        email = login_data.get('email')
        password = login_data.get('password')

        if any([not email, not password]):
            return jsonify({'error': 'Email and password are required.'}), 400

        user = mongo.db.users.find_one({'email': email})

        if not user:
            return jsonify({'error': 'User not found.'}), 404

        if not check_password_hash(user['password'], password):
            return jsonify({'error': 'Incorrect password.'}), 401

        return jsonify({'message': 'Login successful.', 'user': user}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500