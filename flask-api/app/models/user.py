'''  Defines the User model class. '''
from database import db
from flask import jsonify
from .base import BaseModel

class User(db.Model, BaseModel):
    '''
        User model class definition. Inherits BaseModel class.
        
        attributes:
            ID: Number
            username: String
        methods:
            to_json
            create
    '''
    __tablename__ = 'users'

    username = db.Column(db.String(32), unique=True, nullable=False)

    def to_json(self):
        '''
            Returns the JSON representation of a User model.
            Returns: JSON
        '''
        return jsonify({
            'id': self.id,
            'username': self.username
        })

    @staticmethod
    def create(**kwargs):
        '''
            Creates an instance of the User model.
            
            arguments:
                username (optional): String
                ....
            returns: User
        '''
        user = User()
        if 'username' in kwargs:
            user.username = kwargs['username']

        return user
