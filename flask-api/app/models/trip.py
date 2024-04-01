'''  Defines the Trip model class. '''
from datetime import datetime
import json

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, deferred
from sqlalchemy.dialects.postgresql import JSONB

from app.common.errors import ModelException
from app.extensions import db
from app.schema.trip import TripMode
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
            create
            set_points
    '''
    __tablename__ = 'trip'

    # pylint: disable-next=E1136
    name: Mapped[str] = mapped_column(db.String(32), unique=False, nullable=False)
    # pylint: disable-next=E1136
    description: Mapped[str] = mapped_column(db.String(250), unique=False, nullable=True)
    # pylint: disable-next=E1136
    points: Mapped[JSONB] = deferred(mapped_column(JSONB, unique=False, nullable=True))
    # pylint: disable-next=E1136,E1102,C0301
    modified_at: Mapped[datetime] = mapped_column(db.DateTime, unique=False,server_default=func.now())
    # pylint: disable-next=E1136
    user_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
        index=True
    )
    user = db.relationship("User", back_populates="trips")

    @staticmethod
    def create(**kwargs):
        '''
            Creates an instance of the Trip model.
            
            ARGS:
                name (str): The trip's name
                description (str): the trip's description
                user_id (int): The ID of the user the trip belongs to.
            returns:
                Trip - the created trip.
        '''
        trip = Trip()

        if 'name' in kwargs and 'user_id' in kwargs:
            trip.name = kwargs.get('name')
            trip.user_id = kwargs.get('user_id')
            trip.description = kwargs.get('description', None)
        else:
            raise ModelException('Missing name parameter.')
        return trip

    def set_points(self, points: list, mode: TripMode) -> None:
        '''
            Sets the points of the trip.

            ARGS:
                points (list) - The trip points
                mode: TripMode - The trip mode.
        '''
        if isinstance(points, list) and isinstance(mode, TripMode):
            new_points = {
                'points': points,
                'mode': mode
            }

            try:
                self.points = json.dumps(new_points)
            except TypeError as error:
                raise ModelException("Unable to encode trip as json string") from error
        else:
            raise ModelException('Expecting a list of points.')

    def get_points(self):
        '''
            gets the points of the trip.
s
            RETURNS:
                {mode, points}: Mode and points of the trip
        '''
        try:
            points = json.loads(self.points)
            return points
        except json.JSONDecodeError as json_error:
            raise ModelException(f"Unable to load points: {json_error}") from json_error
