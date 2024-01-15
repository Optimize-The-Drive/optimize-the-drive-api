'''
    Houses the Base Schema
'''

from typing import Any

from marshmallow import Schema,  ValidationError

from app.common.errors import SchemaException

class BaseSchema(Schema):
    '''
        Base Schema, overwriting default handle error function.
    '''
    def handle_error(self, error: ValidationError, data: Any, *, many: bool, **kwargs):
        raise SchemaException(error.messages_dict)
