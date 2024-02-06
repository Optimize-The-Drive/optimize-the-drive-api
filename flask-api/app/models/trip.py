'''  Defines the Trip model class. '''
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from app.common.errors import ModelException
from app.extensions import db
from .base import BaseModel


class Trip(db.Model, BaseModel):
    '''
        Trip model class definition. Inherits BaseModel class.
        
        attributes:
            ID: Number
            name: String
            description: String
            points: jsonb
            modified_at: Date
            user_id: User
        methods:
            to_json
            create
    '''
    __tablename__ = 'trip'

    # pylint: disable-next=E1136
    name: Mapped[str] = mapped_column(db.String(32), unique=True, nullable=False)
    # pylint: disable-next=E1136
    description: Mapped[str] = mapped_column(db.String(250), unique=True, nullable=True)
    # pylint: disable-next=E1136
    points: Mapped[str] = mapped_column(JSONB , unique=False, nullable=False)
    # pylint: disable-next=E1136
    modified_at: Mapped[datetime] = mapped_column(db.DateTime, unique=False, default=datetime.now)
    # pylint: disable-next=E1136
    user_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
        index=True
    )
    user = db.relationship("User", back_populates="trips")

    def to_obj(self, with_points=True) -> dict:
        '''
            Returns the JSON representation of a Trip model.

            RETURNS:
                dict { id, name, description, modified_at, points }
        '''

        trip = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'modified_at': self.modified_at,
        }

        if with_points:
            trip['points'] = self.points

        return trip

    @staticmethod
    def create(**kwargs):
        '''
            Creates an instance of the Trip model.
            
            ARGS:
                name (str): The route's name
            returns:
                Trip - the created trip.
        '''
        trip = Trip()

        if 'name' in kwargs:
            trip.name = kwargs.get('name')
        else:
            raise ModelException('Missing name parameter.')
        return trip

    def set_points(self, points: list) -> None:
        '''
            Sets the points of the route.

            ARGS:
                points (list) - The route points
        '''
        if points:
            points = {
                'points': list
            }

            self.points = points

        raise ModelException('Expecting a list of points. Recieved none.')
