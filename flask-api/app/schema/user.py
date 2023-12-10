'''Defines user schemas.'''

from datetime import datetime

from marshmallow import Schema, fields

class UserSchema(Schema):
    '''The User Schema.'''
    id: int = fields.Int(dump_only=True)
    username: str = fields.Str(required=True)
    password: str = fields.Str(required=True, load_only=True)
    created_at: datetime = fields.Str(dump_only=True)
    email: str = fields.Str(dump_only=True)
    