'''  Defines the JWT model class. '''

from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.common.errors import ModelException
from database import db
from .base import BaseModel

class JWTType(Enum):
    '''
        Enum defining the type of JWT
    '''
    REFRESH = 'REFRESH'
    ACCESS = 'ACCESS'


class JWT(db.Model, BaseModel):
    '''
        JWT model class definition. Inherits BaseModel class.
        Stores valid and invalidated JWTs.
        
        attributes:
            ID: Number
            type: Str
        methods:
            to_json
            create
    '''
    __tablename__ = 'jwt'

    jti: Mapped[str] = mapped_column(db.String(36), unique=True, nullable=False)
    type: JWTType = mapped_column(db.Enum(JWTType))
    user_id = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    revoked_at = mapped_column(db.DateTime)
    expires = mapped_column(db.DateTime, nullable=False)

    user = db.relationship("User")

    @staticmethod
    def create(**kwargs):
        '''
            Creates an instance of the JWT model.
            
            arguments:
                jti: String
                type: JWTType
                user_id: Number
                expires: DateTime
            returns: User
        '''
        jwt = JWT()

        if 'jti' and 'type' and 'user_id' and 'expires' in kwargs:
            jwt.jti = kwargs['jti']
            jwt.type = kwargs['type']
            jwt.user_id = kwargs['user_id']
            jwt.expires = kwargs['expires']
        else:
            raise ModelException('missing jti, type, user_id, or expires parameters.')
        return jwt

    def to_obj(self) -> dict:
        '''Not Implemented'''
