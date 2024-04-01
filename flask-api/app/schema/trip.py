'''Schema definition for a Trip'''
from enum import IntEnum
from marshmallow import fields, validate
from app.schema.base import BaseSchema

class TripMode(IntEnum):
    ''' 
        Enum defining the Mode of the trip
    '''
    FIRST_LAST = 0
    ROUND_TRIP = 1

class TripCreateSchema(BaseSchema):
    """
        The route creation schema.
    """
    name: str = fields.Str(required=True, load_only=True, validate=validate.Length(min=1, max=128))
    description: str = fields.Str(required=False, validate=validate.Length(min=0, max=512))


class TripEditSchema(BaseSchema):
    """
        The route creation schema.
    """
    name: str = fields.Str(required=False, load_only=True, validate=validate.Length(min=1, max=128))
    description: str = fields.Str(required=False, validate=validate.Length(min=0, max=512))


class TripPointSchema(BaseSchema):
    """Schema for a trip point."""
    lat = fields.Number(required=True, validate=validate.Range(-90, 90))
    lon = fields.Number(required=True, validate=validate.Range(-180, 180))


class TripOptimizeSchema(BaseSchema):
    """Schema for a trip optimize socketio calls."""
    trip_id: int = fields.Int(required=True)
    points = fields.Nested(
        TripPointSchema,
        required=True, many=True, validate=validate.Length(min=3, max=50)
    )
    mode: TripMode = fields.Enum(TripMode, required=True, by_value=True)


class TripResultSchema(BaseSchema):
    """
        The route result schema.
    """
    trip = fields.Nested({
        'id': fields.Int(dump_only=True),
        'name': fields.Str(required=True, dump_only=True),
        'description': fields.Str(required=True, dump_only=True),
        'points': fields.List(fields.Nested(TripPointSchema), required=False),
        'modified_at': fields.DateTime(dump_only=True)
    })
