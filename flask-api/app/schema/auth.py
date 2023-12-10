'''Defines Auth schemas.'''

from marshmallow import Schema, fields

class LoginSchema(Schema):
    '''The User Schema.'''
    username: str = fields.Str(required=True, load_only=True)
    password: str = fields.Str(required=True, load_only=True)
