#!/usr/bin/env python3
"""authentication template module
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """this function ensures authentication"""
        return False


    def authorization_header(self, request=None) -> str:
        """this function add authorization header"""
        return None


    def current_user(self, request=None) -> TypeVar('User'):
        """this method gets the current user"""
        None
