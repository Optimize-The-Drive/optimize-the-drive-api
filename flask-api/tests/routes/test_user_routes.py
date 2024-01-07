'''
    Defines user route tests
'''

import pytest

from tests.helpers import user_repo


# User CREATE tests HERE
#######################

@pytest.mark.parametrize(
    'auth_client',
    [{'username': 'testuserdelete', 'password': 'testuserdeletepassword'}]
    , indirect=True
)
@pytest.mark.usefixtures("app_ctx")
def test_user_delete(auth_client):
    '''
        Tests that user deletion route as intended.
        
        DELETE /api/user/me
    '''
    client, headers = auth_client

    response = client.delete('/api/user/me', headers={'Authorization': headers['Authorization']})
    response1 = client.post('/api/auth/logout', headers={'Authorization': headers['Authorization']})

    user = user_repo.by_username('testuserdelete')

    assert response.status_code == 200 and response1.status_code == 401 and user is None



def test_user_delete_guarded(client):
    '''
        Tests that the user deletion route is protected.

        DELETE /api/user/me
    '''

    response = client.delete('/api/user/me')

    assert response.status_code == 401
