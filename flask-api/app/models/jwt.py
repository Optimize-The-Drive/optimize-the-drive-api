'''  Defines the JWT model class. '''

from datetime import datetime
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column

from app.common.errors import ModelException
from app.extensions import db
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
        Stores invalidated JWTs.
        
        attributes:
            id (int): database row ID of the JWT.
            jti (str): jti identifier of the JWT.
            type: (JWTType): Type of JWT (access or refresh)
            user_id (int): User that the JWT belongs to.
            expires (datetime): Time that the JWT expires.
        methods:
            to_json
            create
    '''
    __tablename__ = 'jwt'
    # Disabling for pylint bug
    # pylint: disable-next=E1136
    jti: Mapped[str] = mapped_column(db.String(36), unique=True, nullable=False)
    # pylint: disable-next=E1136
    type: Mapped[JWTType] = mapped_column(db.Enum(JWTType), nullable=False)
    # pylint: disable-next=E1136
    user_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
        index=True
    )
    # pylint: disable-next=E1136
    expires: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)

    user = db.relationship("User")

    @staticmethod
    def create(**kwargs):
        '''
            Creates an instance of the JWT model.
            
            ARGS:
                jti (str): JTI of the JWT
                type (JWTType): Type of the JWT
                user_id (int): Id of the user
                expires (datetime): Expiring time of the JWT
            RETURNS:
                JWT - the created JWT
        '''
        jwt = JWT()

        if 'jti' in kwargs and 'type' in kwargs and 'user_id' in kwargs and 'expires' in kwargs:
            jwt.jti = kwargs['jti']
            jwt.type = kwargs['type']
            jwt.user_id = kwargs['user_id']
            jwt.expires = kwargs['expires']
        else:
            raise ModelException('Missing jti, type, user_id, or expires parameters.')
        return jwt

    def to_obj(self) -> dict:
        '''Not Implemented'''
