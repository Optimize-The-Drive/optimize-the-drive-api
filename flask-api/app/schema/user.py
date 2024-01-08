'''Defines user schemas.'''

from datetime import datetime

from marshmallow import Schema, fields, validate


class UserRegex:
    '''
        Common User Schema REGEX strings.
    '''
    USERNAME = r'^[aA-zZ0-9.]{5,}$'
    PASSWORD = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
    EMAIL = r'^\S+@\S+\.\S+$'


class UserAuthSchema(Schema):
    '''The User auth schema.'''
    username: str = fields.Str(required=True, load_only=True)
    password: str = fields.Str(required=True, load_only=True)


class UserRegisterSchema(Schema):
    '''The User register schema.'''
    username: str = fields.Str(
        required=True, load_only=True,
        validate=validate.Regexp(UserRegex.USERNAME)
    )
    password: str = fields.Str(
        required=True, load_only=True,
        validate=validate.Regexp(UserRegex.PASSWORD)
    )
    email: str = fields.Str(
        required=True, load_only=True,
        validate=validate.Regexp(UserRegex.EMAIL)
    )


class UserResponseSchema(Schema):
    '''The User schema found in responses .'''
    id: int = fields.Int(dump_only=True)
    username: int = fields.Str(dump_only=True)
    email: int = fields.Str(dump_only=True)
    created_at: datetime = fields.Str(dump_only=True)
