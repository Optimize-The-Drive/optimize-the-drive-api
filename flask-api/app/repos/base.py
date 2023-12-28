'''
    Repository class with common actions.
'''
from flask_sqlalchemy import SQLAlchemy

from app.extensions import db

class BaseRepo:
    '''
        BaseRepo class definition.

        attributes:
            _db: The database connection of the repo.

        methods:
            add_one
            add_many
            commit
    '''
    _db: SQLAlchemy= db

    def add(self, asset: object or list):
        ''' 
            Adds single / multiple assets to the database.
            
            arguments:
                asset: object or list(object)
        '''
        self._db.session.add(asset)

    def commit(self):
        ''' Commits the assets to the database. '''
        self._db.session.commit()
