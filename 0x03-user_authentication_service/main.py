#!/usr/bin/env python3
"""Testcases for user authentication service through the API"""
from requests import delete, get, post, put

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
URL = 'http://localhost:5000'
url_users = f'{URL}/users'
url_sessions = f'{URL}/sessions'
url_profile = f'{URL}/profile'
url_logout = f'{URL}/logout'
url_reset_pwd = f'{URL}/reset_password'


def register_user(email: str, password: str) -> None:
    """Tests user registration"""
    response = post(url_users, {'email': email, 'password': password})
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'user created'}


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests user login with correct email and wrong password"""
    response = post(url_sessions, {'email': email, 'password': password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Tests user login with correct credentials"""
    response = post(url_sessions, {'email': email, 'password': password})
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'logged in'}
    assert response.cookies.get('session_id')
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """Tests profile route when no user is logged-in"""
    response = get(url_profile)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Tests profile route with valid session_id for a logged-in user"""
    response = get(url_profile, cookies={'session_id': session_id})
    assert response.status_code == 200
    assert response.json().get('email')


def log_out(session_id: str) -> None:
    """Tests user registration"""
    response = delete(url_sessions, cookies={'session_id': session_id})
    assert response.json() == {'message': 'Bienvenue'}
    assert response.history
    assert response.history[0].status_code == 302


def reset_password_token(email: str) -> str:
    """Tests user registration"""
    response = post(url_reset_pwd, {'email': email})
    assert response.status_code == 200
    reset_token = response.json().get('reset_token')
    assert response.json() == {'email': email, 'reset_token': reset_token}
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests user registration"""
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    response = put(url_reset_pwd, data)
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'Password updated'}


if __name__ == '__main__':
    """Runs the code in this module"""
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
