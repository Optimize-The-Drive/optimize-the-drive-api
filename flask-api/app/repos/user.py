'''
    Defines the user repository.
'''
from app.models.user import User
from .base import BaseRepo


class UserRepo(BaseRepo):
    '''
		JWTRepo defintion. Extends the BaseRepository.

		methods:
			by_jti
	'''
    def by_id(self, user_id: int) -> User:
        '''
            Returns the user by it's ID.

            arguments:
                user_id: int

            returns: User
        '''
        return self._db.session.execute(
            self._db.select(User).filter_by(id=user_id)
        ).scalar()

    def by_username(self, username: str) -> User:
        '''
            Returns the user by it's username.

            arguments:
                username: str

            returns: User
        '''
        return self._db.session.execute(
            self._db.select(User).filter_by(username=username)
        ).scalar()
    