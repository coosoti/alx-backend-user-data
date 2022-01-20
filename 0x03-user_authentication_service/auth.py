#!/usr/bin/env python3
"""
User Authentication module
"""

from bcrypt import hashpw, gensalt
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """this method takes password and return salted hash of the password"""
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """this method returns a string representation of a new UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """this method create new user and save to the db and return
        User object"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """this function locates user by email and check if password matches
        with bcrypt.checkpw and return True else return False"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """this method locate user by email, generate new UUID and store it
        in the db as user's session_id, then returns session ID"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return
