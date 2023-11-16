#!/usr/bin/env python3
"""User authentication service with SQLAlchemy for database abstraction"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from typing import Any
from user import Base, User


class DB:
    """DB class"""
    def __init__(self) -> None:
        """Initialize a new DB instance"""
        # self._engine = create_engine('sqlite:///a.db', echo=True)
        self._engine = create_engine('sqlite:///a.db')
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Creates a new user in the database and returns it"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    # def find_user_by(self, **attributes: dict) -> list:
    def find_user_by(self, **attributes: Any) -> User:
        """Searches for a user in the database using the given attribute(s)"""
        result = self._session.query(User).filter_by(**attributes).all()
        if not result:
            raise NoResultFound
        return result[0]

    def update_user(self, user_id: int, **attributes: dict) -> None:
        """Updates a user in the database using the given id"""
        # Search for user with user_id in database
        user = self.find_user_by(id=user_id)
        if not user:
            print(f'Error! User with id={user_id} not found')
            return

        # Validate given attributes before updating user
        valid = [str(attr).split('.')[1] for attr in User.__table__.columns]
        for key in attributes.keys():
            if key not in valid:
                raise ValueError(f'{key} is not an attribute of User')

        # Update user's attributes in database
        for key in attributes.keys():
            setattr(user, key, attributes[key])
        self._session.commit()


if __name__ == '__main__':
    """Tests the code in this module"""
    from sys import stderr
    my_db = DB()

    user_1 = my_db.add_user('test@test.com', 'SuperHashedPwd')
    user_2 = my_db.add_user('test1@test.com', 'SuperHashedPwd1')

    def test_exceptions(**kwargs: Any) -> None:
        from sqlalchemy.exc import InvalidRequestError
        try:
            print(my_db.find_user_by(**kwargs))
        except NoResultFound:
            print('Error! No user with email==user_2.email', file=stderr)
        except InvalidRequestError as e:
            print('Error!', e.args[0], file=stderr)

    test_exceptions(email='user_2.email')
    test_exceptions(fake_arg='user_2.email')

    user = my_db.find_user_by(email=user_2.email)
    print(user.id, user.email, user.hashed_password, user.session_id)

    try:
        my_db.update_user(user_id=1, email='wow@w.w', pee='#noP')
    except ValueError as e:
        print('ValueError!', e.args[0], file=stderr)
    user = my_db.find_user_by(id=1)
    print(user.id, user.email, user.hashed_password, user.session_id)
    print(user.__dict__)
