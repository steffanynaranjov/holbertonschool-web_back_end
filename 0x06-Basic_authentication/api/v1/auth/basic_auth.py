#!/usr/bin/env python3
""" Basic Authorization """

import base64
from typing import Tuple, TypeVar

from werkzeug.wrappers import AuthorizationMixin
from api.v1.auth.auth import Auth
from models.user import User
import json


class BasicAuth(Auth):
    """ Basic Authorization"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Basic - Base64 part """
        try:
            if authorization_header and isinstance(authorization_header, str):
                if 'Basic ' in authorization_header:
                    if authorization_header[0:6] == 'Basic ':
                        return authorization_header[6:]
        except Exception:
            return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Base64 decode """
        if base64_authorization_header and \
                isinstance(base64_authorization_header, str):
            try:
                return base64.b64decode(base64_authorization_header).decode()
            except Exception:
                return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        User credentials
        Return: tuple
        """
        if decoded_base64_authorization_header and \
                isinstance(decoded_base64_authorization_header, str):
            if ':' in decoded_base64_authorization_header:
                return tuple(decoded_base64_authorization_header.split(':', 1))
        return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ User Object """
        try:
            if user_email and isinstance(user_email, str) and \
                    user_pwd and isinstance(user_pwd, str):
                user = User.search({'email': user_email})
                if user[0].is_valid_password(user_pwd):
                    return user[0]
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ return user """
        authorization = self.authorization_header(request)
        auth_header = self.extract_base64_authorization_header(authorization)
        decode_auth = self.decode_base64_authorization_header(auth_header)
        email, password = self.extract_user_credentials(decode_auth)
        current_usr = self.user_object_from_credentials(email, password)
        return current_usr
