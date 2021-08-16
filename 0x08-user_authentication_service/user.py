#!/usr/bin/env python3
"""
authorization file
"""

import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """ function that tranform a string to hash """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _generate_uuid() -> str:
    """ function that generate a UUID """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ method constructor """
        self._db = DB()
        self.__id = None

    def register_user(self, email: str, password: str) -> User:
        """ method that register a new user """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            hash_pwd = _hash_password(password)
            return self._db.add_user(email=email, hashed_password=hash_pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """ method that check if the user is correct """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                    password.encode(), user.hashed_password.encode()
                )
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """method that create a new Session ID """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ method that get a user by session ID"""
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ method that destroy a session """
        if not user_id:
            return None

        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ methoh that generate a token """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)

            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updates a user password to a provided password """
        if not reset_token or not password:
            return None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
