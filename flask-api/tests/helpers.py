'''
    Helper functions for tests.
'''

from app.extensions import db
from app.models.user import User

def add_user_to_db(username: str, email: str, password: str):
    '''
        Adds a user to the database.

        ARGS:
            username (str): The username of the user
            email (str): The email of the user
            password (str): The password of the user
        RETURNS:
            User - the created user.
    '''
    user = User.create(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return user

def remove_user_from_db(user: User):
    '''
        Removes a user from the database.

        ARGS:
            User (user): The user to remove
    '''
    db.session.delete(user)
    db.session.commit()
