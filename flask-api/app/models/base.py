''' Defines the base model class. '''
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db


class BaseModel():
    '''
        Base model class definition.
        
        attributes:
            id (int): database row ID of the model.
        methods:
            abstract create
    '''
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)

    @staticmethod
    def create(**kwargs):
        '''
            Abstract create method for a model.
            
            RETURNS NotImplementedError.
        '''
        raise NotImplementedError("Please implement this method")
