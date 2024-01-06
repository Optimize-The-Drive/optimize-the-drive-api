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

            ARGS:
                user_id (int): The user's ID

            RETURNS:
                User - The queried User.
        '''
        return self._db.session.execute(
            self._db.select(User).filter_by(id=user_id)
        ).scalar()

    def by_username(self, username: str) -> User:
        '''
            Returns the user by it's username.

            ARGS:
                username (str): The user's username

            RETURNS:
                User - The queried User.
        '''
        return self._db.session.execute(
            self._db.select(User).filter_by(username=username)
        ).scalar()
    