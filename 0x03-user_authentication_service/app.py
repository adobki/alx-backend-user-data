#!/usr/bin/env python3
"""API for user authentication service"""
from flask import Flask, jsonify, abort, make_response, request, redirect
from flask_cors import CORS
from auth import Auth


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
AUTH = Auth()


@app.route('/')
def home() -> str:
    """Home/default route"""
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """User sign-up route"""
    # Retrieve values from HTML form fields
    email = request.form.get('email')
    pwd = request.form.get('password')
    # Input validation
    if not email:
        return jsonify({'error': 'No email'}), 400
    if not pwd:
        return jsonify({'error': 'No password'}), 400
    # Create new user if user with email doesn't exist
    try:
        AUTH.register_user(email=email, password=pwd)
        return jsonify({'email': email,
                        'message': 'user created'})
    except ValueError:
        # Return error as user with email already exists
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """User login route"""
    # Retrieve values from HTML form fields
    email = request.form.get('email')
    pwd = request.form.get('password')

    # Validate provided user credentials
    if not email or not pwd or not AUTH.valid_login(email=email, password=pwd):
        abort(401)

    # Log user in
    session_id = AUTH.create_session(email=email)
    response = make_response(jsonify({'email': email, 'message': 'logged in'}))
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """User logout route"""
    # Retrieve session_id from cookie data in request
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    # Find user with session_id and logout if exists
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    # Log user out and return to homepage
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """User profile info route"""
    # Retrieve session_id from cookie data in request
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    # Find user with session_id and logout if exists
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    # Return user profile information
    return jsonify({'email': user.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password() -> str:
    """User password reset - Generate password reset token"""
    # Retrieve email from HTML form field
    email = request.form.get('email')
    if not email:
        abort(403)
    # Find user with email and create reset token if exists
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({'email': email, 'reset_token': reset_token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """User password reset - Update password with reset token"""
    # Retrieve email from HTML form fields
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    if not email or not reset_token or not new_password:
        abort(403)
    # Update user's password if reset token is valid
    try:
        AUTH.update_password(reset_token, password=new_password)
        return jsonify({'email': email, 'message': 'Password updated'})
    except ValueError:
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
