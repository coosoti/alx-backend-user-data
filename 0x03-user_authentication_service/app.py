#!/usr/bin/env python3
"""
API Route Module
"""

from flask import Flask, abort, jsonify, request
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """returns a JSON payload"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """this method registers new users -> POST /users"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        new_user = AUTH.register_user(email, password)
        if new_user is not None:
            return jsonify({
                "email": f"{email}",
                "message": "user created"
            }), 200
    except Exception:
        return jsonify({
            "message": "email already registered"
        }), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """this function creates a new session for the user, store it in the
    session ID as a cookie with key "session_id" and returns JSON payload"""
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)

    if not valid_login:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": f"{email}", "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
