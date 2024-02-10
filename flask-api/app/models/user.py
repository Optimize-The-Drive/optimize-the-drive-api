'''  Defines the User model class. '''
from datetime import datetime

from passlib.hash import bcrypt_sha256
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from app.common.errors import ModelException
from app.extensions import db
from .base import BaseModel


class User(db.Model, BaseModel):
    '''
        User model class definition. Inherits BaseModel class.
        
        attributes:
            ID: Number
            username: String
            email: String
            password_hash: String
            created_at: DateTime
            verified: Boolean
        methods:
            create
            set_password
            validate_password
    '''
    __tablename__ = 'users'

    # pylint: disable-next=E1136
    username: Mapped[str] = mapped_column(db.String(32), unique=True, nullable=False)
    # pylint: disable-next=E1136
    email: Mapped[str] = mapped_column(db.String(128), unique=True, nullable=False)
    # pylint: disable-next=E1136
    password_hash: Mapped[str] = mapped_column(db.String(128), unique=False, nullable=False)
    # pylint: disable-next=E1136,E1102,C0301
    created_at: Mapped[datetime] = mapped_column(db.DateTime, unique=False, server_default=func.now())
    # pylint: disable-next=E1136,C0301
    verified: Mapped[bool] = mapped_column(db.Boolean, unique=False, nullable=False, server_default=expression.false())

    jwts = db.relationship("JWT", cascade="all,delete", back_populates="user")
    trips = db.relationship("Trip", cascade="all,delete", back_populates="user")

    @staticmethod
    def create(**kwargs):
        '''
            Creates an instance of the User model.
            
            ARGS:
                username (str): The user's username
                email (str): The user's email.
            returns:
                User - the created user.
        '''
        user = User()

        if 'username' in kwargs and 'email' in kwargs:
            user.username = kwargs['username']
            user.email = kwargs['email']
            user.verified = False
        else:
            raise ModelException('Missing username or email parameters.')
        return user

    def set_password(self, plaintext: str = '') -> None:
        '''
            Sets the password of the user, encrypting it.
            
            ARGS:
                plaintext (str): unencrypted password
        '''
        self.password_hash = bcrypt_sha256.hash(plaintext)

    def verify_password(self, plaintext: str = '') -> bool:
        '''
            Verifies the password of the user.
            
            ARGS:
                plaintext (str): unencrypted password
            RETURNS:
                Boolean - whether the password is correct or not.
        '''
        return bcrypt_sha256.verify(plaintext, self.password_hash)
