''' Defines the base model class. '''
from database import db


class BaseModel():
    '''
        Base model class definition.
        
        attributes:
            ID: Number
        methods:
            abstract to_json
            abstract create
    '''
    id = db.Column(db.Integer, primary_key=True)

    def to_json(self):
        '''
            Abstract to_json method for a model.
            
            Returns NotImplementedError.
        '''
        raise NotImplementedError("Please implement this method")

    @staticmethod
    def create(**kwargs):
        '''
            Abstract create method for a model.
            
            Returns NotImplementedError.
        '''
        raise NotImplementedError("Please implement this method")
