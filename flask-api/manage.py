'''
    Command line utiliy for the flask api.
'''
from flask.cli import FlaskGroup
from server import app
from app import db
from app.models.user import User

cli = FlaskGroup(app)

@cli.command('init_dev_db')
def init_db():
    '''
        Initializes the database with mock data.
    '''
    try:
        user = User.create(username='otduser', email='otduser@email.com')
        user.set_password('otdpassword')
        db.session.add(user)
        db.session.commit()
    # pylint: disable-next=W0718
    except Exception as e:
        print('Skipping data initialization due to: ', e)


@cli.command('init_test_db')
def init_test_db():
    '''
        Initializes the database with mock data.
    '''
    try:
        user = User.create(username='test-user', email='test-email@gmail.com')
        user.set_password('test-password')
        db.session.add(user)
        db.session.commit()
    # pylint: disable-next=W0718
    except Exception as e:
        print('Skipping data initialization due to: ', e)

if __name__ == '__main__':
    cli()
