'''Defines user schemas.'''

from datetime import datetime

from marshmallow import Schema, fields


class UserAuthSchema(Schema):
    '''The User auth schema.'''
    username: str = fields.Str(required=True, load_only=True)
    password: str = fields.Str(required=True, load_only=True)

class UserRegisterSchema(UserAuthSchema):
    '''The User register schema.'''
    email: str = fields.Str(required=True, load_only=True)

class UserResponseSchema(Schema):
    '''The User schema found in responses .'''
    id: int = fields.Int(dump_only=True)
    username: int = fields.Str(dump_only=True)
    email: int = fields.Str(dump_only=True)
    created_at: datetime = fields.Str(dump_only=True)

# username_valid(username: str) -> 