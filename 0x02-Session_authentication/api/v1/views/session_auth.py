#!/usr/bin/env python3
"""
Session Views Module
"""

from os import getenv
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def login() -> str:
    """session login view for /auth_session/login """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"})
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth
        _my_session_id = auth.create_session(user[0].id)
        json_res = jsonify(user[0].to_json(True))
        session_name = getenv("SESSION_NAME")
        json_res.set_cookie(session_name, _my_session_id)
        return json_res


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """session logout view for route /auth_session/logout"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
