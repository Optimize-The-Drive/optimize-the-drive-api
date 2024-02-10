'''
	Defines the Trip repository.
'''
from app.models.trip import Trip
from .base import BaseRepo


class TripRepo(BaseRepo):
    '''
        Trip Repo definition. Extends the Base Repository.

        methods:
            by_user_id
    '''
    def by_user_id(self, user_id: int):
        '''
            Returns all trips belonging to a specific user.
            
            ARGS:
                user_id (int): The user ID.
            RETURNS:
                Trip List or None - The lists belonging to the user.
        '''
        return self.execute(self._db.select(Trip).filter_by(user_id=user_id)).scalars().all()
 