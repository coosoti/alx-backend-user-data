#!/usr/bin/env python3
"""
API Route Module
"""

from flask import Flask, abort, jsonify, redirect, request
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


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """this method finds the user with requested session ID, destroys the
    session and redirect the user to GET /"""
    cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(cookie)
    if cookie is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """this method gets user by using the session_id"""
    cookie = request.cookies.get("session_id", None)
    if cookie is None:
        abort(403)
    user = AUTH.get_user_from_session_id(cookie)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
