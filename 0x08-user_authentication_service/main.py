#!/usr/bin/env python3
"""
Main file
"""
import requests

URL = 'http://127.0.0.1:5000'
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """
    function that valida if a
    request is correct and the user is correctly rigistered"""
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(f'{URL}/users', data=data)
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'user created'}


def log_in_wrong_password(email: str, wrong_passwd: str) -> None:
    """ function that check login with wrong password """
    data = {
        'email': email,
        'password': wrong_passwd
    }
    response = requests.post(f'{URL}/sessions', data=data)
    assert response.status_code == 401


def profile_unlogged():
    """ function that verify is a user is unlogged """
    cookie = {'session_id': None}
    response = requests.get(f'{URL}/profile', cookies=cookie)
    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    """ function that check if a user is logged """
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(f'{URL}/sessions', data=data)
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'logged in'}
    session_id = response.cookies.get('session_id')
    return session_id


def profile_logged(session_id: str) -> None:
    """ profile logged """
    cookie = {'session_id': session_id}
    response = requests.get(f'{URL}/profile', cookies=cookie)
    assert response.status_code == 200
    assert response.json() == {'email': EMAIL}


def log_out(session_id: str) -> None:
    """ function that check if user is logout """
    cookie = {'session_id': session_id}
    response = requests.delete(f'{URL}/sessions', cookies=cookie)
    assert response.status_code == 200
    assert response.json() == {'message': 'Bienvenue'}


def reset_password_token(email: str) -> str:
    """ function that check if the password was reset """
    data = {'email': email}
    response = requests.post(f'{URL}/reset_password', data=data)
    assert response.status_code == 200
    token = response.json()
    return token.get('reset_token')


def update_password(email: str, token: str, new_passwd: str) -> None:
    """ function that check if the update password is success """
    data = {
        'email': email,
        'reset_token': token,
        'new_password': new_passwd
    }
    response = requests.put(f'{URL}/reset_password', data=data)
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'Password updated'}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
