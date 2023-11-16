#!/usr/bin/env python3
"""User class model/template for user authentication service"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """SQLAlchemy model for database table `users`"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))

    def __repr__(self):
        """String representation of object"""
        s_id = 'Yes' if self.session_id else 'No'
        return f'<User(id={self.id}, email={self.email}, session_id={s_id})>'


if __name__ == '__main__':
    """Tests the code in this module"""
    print(User.__tablename__)
    for column in User.__table__.columns:
        print('{}: {}'.format(column, column.type))

    print(User())
    print(User(id=98, email='email@mail.com',
               hashed_password='pwd', session_id=True))
