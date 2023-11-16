#!/usr/bin/env python3
"""Module for user management and authentication"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Salts and hashes a password"""
    if password is not None and isinstance(password, str):
        return bcrypt.hashpw(bytes(password, 'UTF-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a unique id string"""
    return uuid4().__str__()


class Auth:
    """Auth class to interact with the authentication database"""
    def __init__(self):
        """Initialises an instance of this class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Adds a new user to the database"""
        # Input validation
        if not email or not isinstance(email, str)\
                or not password or not isinstance(password, str):
            return None

        # Check if a user with given email already exists in database
        from sqlalchemy.orm.exc import NoResultFound
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            # Create and return new user with email and hashed password
            return self._db.add_user(email,
                                     _hash_password(password).decode('utf-8'))

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user's credentials for logging-in"""
        # Input validation
        if email and isinstance(email, str)\
                and password and isinstance(password, str):
            # Check if a user with given credentials exists in database
            from sqlalchemy.orm.exc import NoResultFound
            try:
                # Validate provided email
                user = self._db.find_user_by(email=email)
                # Validate provided password and return result
                return bcrypt.checkpw(bytes(password, 'UTF-8'),
                                      bytes(user.hashed_password, 'UTF-8'))
            except NoResultFound:
                # Invalid email - exit try block and return False
                pass
        return False

    def create_session(self, email: str) -> str:
        """Login method: Creates a new session for an authenticated user"""
        # Input validation
        if not email or not isinstance(email, str):
            return None

        # Check if a user with given email exists in database
        from sqlalchemy.orm.exc import NoResultFound
        try:
            user = self._db.find_user_by(email=email)

            # Create new session_id and assign it to the user, then return it
            self._db.update_user(user.id, session_id=_generate_uuid())
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Searches for a user in the database for a given session_id"""
        # Input validation
        if not session_id or not isinstance(session_id, str):
            return None

        # Search for user in the database and return the result
        from sqlalchemy.orm.exc import NoResultFound
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Searches for a user in the database for a given session_id"""
        # Input validation
        if not user_id or not isinstance(user_id, int):
            return None

        # Search for user in the database and return the result
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Creates a password reset token"""
        # Input validation
        if not email or not isinstance(email, str):
            return None

        # Check if a user with given email exists in database
        from sqlalchemy.orm.exc import NoResultFound
        try:
            user = self._db.find_user_by(email=email)

            # Create reset token and assign it to the user, then return it
            self._db.update_user(user.id, reset_token=_generate_uuid())
            return user.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Changes a user's password using a reset token"""
        # Input validation
        if not reset_token or not isinstance(reset_token, str)\
                or not password or not isinstance(password, str):
            raise ValueError

        # Check if a user with given reset_token exists in database
        from sqlalchemy.orm.exc import NoResultFound
        try:
            user = self._db.find_user_by(reset_token=reset_token)

            # Hash and update password then clear reset_token
            self._db.update_user(
                user.id, reset_token=None, session_id=None,
                hashed_password=_hash_password(password).decode('utf-8')
            )
        except NoResultFound:
            raise ValueError
