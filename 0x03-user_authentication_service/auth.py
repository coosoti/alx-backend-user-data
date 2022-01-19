#!/usr/bin/env python3
"""
User Authentication module
"""

from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """this method takes password and return salted hash of the password"""
    return hashpw(password.encode('utf-8'), gensalt())
