
from database import db


class BaseModel():
    id = db.Column(db.Integer, primary_key=True)
    
    def to_json(self):
        raise NotImplementedError("Please implement this method")
    
    @staticmethod
    def create(**kwargs):
        raise NotImplementedError("Please implement this method")
