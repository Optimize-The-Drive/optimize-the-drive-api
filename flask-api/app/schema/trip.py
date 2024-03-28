'''Schema definition for a Trip'''

from marshmallow import fields, validate
from app.schema.base import BaseSchema


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
    lat: int = fields.Int(required=True, dump_only=True)
    lon: int = fields.Int(required=True, dump_only=True)


class TripResultSchema(BaseSchema):
    """
        The route result schema.
    """
    trip = fields.Nested({
        'id': fields.Int(dump_only=True),
        'name': fields.Str(required=True, dump_only=True),
        'description': fields.Str(required=True, dump_only=True),
        'points': fields.Nested(TripPointSchema(), required=False),
        'modified_at': fields.DateTime(dump_only=True)
    })
