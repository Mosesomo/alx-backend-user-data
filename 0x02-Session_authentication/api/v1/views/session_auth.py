#!/usr/bin/env python3
'''session view'''
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def auth_session():
    '''handles session authentication'''
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == []:
        return jsonify({'error': 'email missing'}), 400
    if password is None or password == []:
        return jsonify({'error': 'password missing'}), 400
    users = User.search({'email': email})
    if not users or users == []:
        return jsonify({'error': 'no user found for this email'}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = make_response(jsonify(user.to_json()))
            response.set_cookie(getenv("SESSION_NAME",
                                       "_my_session_id"),
                                session_id)
            return response
        return jsonify({'error': 'wrong password'}), 404


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def delete_session():
    '''logout user'''
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        return jsonify({}), 404
