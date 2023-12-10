''' Defines the base model class. '''
from database import db
from sqlalchemy.orm import Mapped, mapped_column

class BaseModel():
    '''
        Base model class definition.
        
        attributes:
            ID: Number
        methods:
            abstract to_json
            abstract create
    '''
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)

    def to_obj(self) -> dict:
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
