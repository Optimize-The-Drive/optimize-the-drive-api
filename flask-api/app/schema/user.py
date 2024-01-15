'''Defines user schemas.'''

from marshmallow import fields, validate, validates_schema
from marshmallow.exceptions import ValidationError

from app.schema.base import BaseSchema

class UserRegex:
    '''
        Common User Schema REGEX strings.
    '''

    # 5-20 Characters (including . _)
    # No sequentially repeating symbols
    # Symbols cannot be at the beginning or end of the username
    USERNAME = r'^(?=[a-zA-Z0-9._]{5,20}$)(?!.*[_.]{2})[^_.].*[^_.]$'
    # 8-32 characters
    # Contains an uppercase/lowercase letter, number, symbol
    PASSWORD = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,32}$'
    # Email must follow pattern _@_._ and be no more than 128 characters
    EMAIL = r'^\S+@\S+\.\S+$'

class UserAuthSchema(BaseSchema):
    '''The User auth schema.'''
    username: str = fields.Str(required=True, load_only=True)
    password: str = fields.Str(required=True, load_only=True)

class UserRegisterSchema(BaseSchema):
    '''The User register schema.'''
    username: str = fields.Str(
        required=True, load_only=True,
        validate=validate.Regexp(UserRegex.USERNAME)
    )
    password: str = fields.Str(
        required=True, load_only=True,
        validate=validate.Regexp(UserRegex.PASSWORD)
    )
    confirm_password: str = fields.Str(
        required=True, load_only=True,
        validate=validate.Regexp(UserRegex.PASSWORD)
    )
    email: str = fields.Str(
        required=True, load_only=True,
        validate=validate.Regexp(UserRegex.EMAIL)
    )

    @validates_schema
    def validate_schema(self, data, **_kwargs):
        '''
            Confirms that the password and confirm_password fields match.
        '''
        if data['password'] != data['confirm_password']:
            raise ValidationError({'confirm_password': 'Passwords do not match.'})

        if len(data['email']) > 128:
            raise ValidationError({'email': 'Email does not match expected pattern.'})

class UserResponseSchema(BaseSchema):
    '''The User schema found in responses .'''
    user = fields.Nested({
        'id': fields.Int(dump_only=True),
        'username': fields.Str(dump_only=True),
        'email': fields.Str(dump_only=True),
        'created_at': fields.DateTime(dump_only=True)
    })
