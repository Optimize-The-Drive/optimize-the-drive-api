'''
	Defines the JWT repository.
'''
from app.models.jwt import JWT
from .base import BaseRepo


class JWTRepo(BaseRepo):
    '''
        JWT Repo definition. Extends the Base Repository.

        methods:
            by_jti
    '''
    def by_jti(self, jti: str) -> JWT:
        '''
            Queries a JWT token by it's JTI.

            ARGS:
                jti (str): The JTI of the JWT.
            returns:
                JWT - The queried JWT.
        '''
        return self._db.session.execute(
            self._db.select(JWT).filter_by(jti=jti)
        ).scalar()
