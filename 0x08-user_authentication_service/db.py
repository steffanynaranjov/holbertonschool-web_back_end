#!/usr/bin/env python3
""" Database module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from typing import TypeVar

from user import Base
from user import User


class DB:
    """ Database class
        Creates engine, session, adds user object to DB
        Methods:
            add_user - save the user object to the database
            find_user_by - returns the first row found in the users table
    """
    def __init__(self):
        """ constructor"""
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """create session """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar('User'):
        """ Add a user instance to the session DB """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs: dict) -> object:
        """ returns the first row found in the users table
            as filtered by the method’s input arguments
        """
        return self._session.query(User).filter_by(**kwargs).first()

    def update_user(self, user_id: int, **kwargs: dict) -> None:
        """ update the user’s attributes as passed in the method’s arguments
            then commit changes to the database
        """
        u = self.find_user_by(id=user_id)
        for key, val in kwargs.items():
            if not hasattr(u, key):
                raise ValueError
            setattr(u, key, val)
        self._session.commit()
