'''
    Command line utiliy for the flask api.
'''
from flask.cli import FlaskGroup
from server import app
from app import db
from app.models import User

cli = FlaskGroup(app)

@cli.command('init_db')
def init_db():
    '''
        Initializes the database with mock data.
    '''
    # db.drop_all()
    # db.create_all()

    try:
        user = User.create(username='testuser', email='test@email.com')
        user.set_password('test_password')
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print('Skipping data initialization due to: ', e)

if __name__ == '__main__':
    cli()
