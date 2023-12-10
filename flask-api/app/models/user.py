'''  Defines the User model class. '''
from datetime import datetime

from app.common.errors import ModelException
from database import db
from passlib.hash import bcrypt_sha256
from sqlalchemy.orm import Mapped, mapped_column
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
            to_json
            create
            set_password
            validate_password
    '''
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(db.String(32), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String(128), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(128), unique=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(db.DateTime, unique=False, default=datetime.now)
    verified: Mapped[bool] = mapped_column(db.Boolean, unique=False, nullable=False, default=False)

    def to_obj(self) -> dict:
        '''
            Returns the JSON representation of a User model.
            Returns: JSON
        '''
        return {
            'id': self.id,
            'username': self.username,
            'email': self.username,
            'created_at': self.created_at,
            'verified': self.verified
        }

    @staticmethod
    def create(**kwargs):
        '''
            Creates an instance of the User model.
            
            arguments:
                username: String
                email: String
            returns: User
        '''
        user = User()

        if 'username' and 'email' in kwargs:
            user.username = kwargs['username']
            user.email = kwargs['email']
        else:
            raise ModelException('missing username or email parameters.')
        return user

    def set_password(self, plaintext: str) -> None:
        '''
            Sets the password of the user, encrypting it.
            
            arguments:
                plaintext: String
            returns: None
        '''
        self.password_hash = bcrypt_sha256.hash(plaintext)

    def verify_password(self, plaintext: str) -> bool:
        '''
            Verifies the password of the user.
            
            arguments:
                plaintext: String
            returns: Boolean
        '''
        return bcrypt_sha256.verify(plaintext, self.password_hash)
