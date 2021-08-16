#!/usr/bin/env python3
""" making advances to get the percent
"""
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """class Auth"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require auth """
        if path and excluded_paths:
            if path[-1] != '/':
                path += '/'
            for pth in excluded_paths:

                path = path.replace('/', '')
                pth = pth.replace('/', '')

                if pth[-1] == '*':
                    pth = pth.replace('*', '.*')

                if re.search(pth, path):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ header of authorization """
        try:
            if request and request.headers['Authorization']:
                return request.headers['Authorization']
        except KeyError:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ get current user"""
        return None
