#!/usr/bin/env python3
"""
This module contains functions for handling user passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """this function takes a str argument and encodes it returing a
    hashed password which is  a byte string"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
