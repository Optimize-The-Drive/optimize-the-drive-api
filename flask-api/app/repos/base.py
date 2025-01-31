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
            exec
    '''
    _db: SQLAlchemy = db

    def add(self, asset: object or list):
        ''' 
            Adds single / multiple assets to the database.
            
            ARGS:
                asset (object or list (object)): Asset(s) to save to the db.
        '''
        if isinstance(asset, list):
            self._db.session.add_all(asset)
        else:
            self._db.session.add(asset)

    def delete(self, asset: object):
        '''
            Removes an asset from the database.

            ARGS:
                asset (object): Asset to remove from the db.
        '''
        self._db.session.delete(asset)

    def execute(self, statement):
        '''
            Executes a database statement.

            ARGS:
                statement (SqlAlchemy statement): Statement to execute.
                
            RETURNS:
                SqlAlchemy result
        '''
        return self._db.session.execute(statement)

    def commit(self):
        ''' Commits the assets to the database. '''
        self._db.session.commit()
