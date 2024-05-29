#!/usr/bin/env python3
from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from authentication.operation import create_user, get_user_by_email, get_user_by_username, check_user_credentials
from werkzeug.security import generate_password_hash, check_password_hash
from authentication.operation import create_user, get_user_by_email, get_user_by_username, check_user_credentials
from flask_mail import Mail, Message

mail = Mail()  # Instantiate Mail object here

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        # Input validation
        if not email or not username or not password:
            return jsonify({'message': 'Email, username or password is empty!'}), 400

        # Email validation
        # try:
        #     valid = validate_email(email)
        #     email = valid.email
        # except EmailNotValidError as e:
        #     return jsonify({'message': str(e)}), 400

        # Check if user already exists
        if get_user_by_email(email) or get_user_by_username(username):
            return jsonify({'message': 'User already exists!'}), 400

        # Create new user
        hashed_password = generate_password_hash(password)
        create_user(email, username, hashed_password)
        return jsonify({'message': 'User registered successfully!'})

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Input validation
        if not email or not password:
            return jsonify({'message': 'Email or password is empty!'}), 400

        user = get_user_by_email(email)
        if user and check_user_credentials(password, email):
            return jsonify({'message': 'Logged in!'})
        else:
            return jsonify({'message': 'Failed!'}), 401

class AdminRegistration(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        # Input validation
        if not email or not username or not password:
            return jsonify({'message': 'Email, username or password is empty!'}), 400

        # Email validation
        # try:
        #     valid = validate_email(email)
        #     email = valid.email
        # except EmailNotValidError as e:
        #     return jsonify({'message': str(e)}), 400

        # Check if user already exists
        if get_user_by_email(email) or get_user_by_username(username):
            return jsonify({'message': 'User already exists!'}), 400

        # Create new admin user
        hashed_password = generate_password_hash(password)
        create_user(email, username, hashed_password, is_admin=True)
        return jsonify({'message': 'Admin registered successfully!'})