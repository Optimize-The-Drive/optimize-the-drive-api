from database import db
from flask import jsonify
from .base import BaseModel

class User(db.Model, BaseModel):
    
    __tablename__ = 'users'
    
    username = db.Column(db.String(32), unique=True, nullable=False)
    
    def to_json(self):
        return jsonify({
            'id': self.id,
            'username': self.username
        })
        
    @staticmethod
    def create(**kwargs):
        user = User()
        if 'username' in kwargs:
            user.username = kwargs['username']
            
        return user
