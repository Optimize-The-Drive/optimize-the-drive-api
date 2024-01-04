'''
    Defines auth route tests
'''

def test_correct_login(client):
    '''
        Tests that passing a correct username and password logs in correctly.
    '''
    response = client.post(
        '/api/auth/login',
        json={'username': 'test-user', 'password': 'test-password'}
    )

    access = response.json['access_token']
    refresh = client.get_cookie('refresh_token_cookie', path='/api/auth/refresh')

    assert response.status_code == 200
    assert access and refresh


def test_wrong_login(client):
    '''
        Tests that passing in a wrong username/password prevents a user from logging in.
    '''
    req = client.post(
        '/api/auth/login',
        json={'username': 'test-user', 'password': 'wrong-password'}
    )
    req1 = client.post('/api/auth/login', json={
        'username': 'wrong-user', 'password': 'test-password'
    })

    assert req.status_code == 401 and req1.status_code == 401


def test_guarded_refresh(client):
    '''
        Tests that the refresh endpoint is guarded.
    '''

    # No refresh token cookie is passed
    req = client.post('/api/auth/refresh')

    assert req.status_code == 401


def test_refresh(auth_client):
    '''
        Tests that the refresh endpoint returns an access_token.
    '''
    client, _access_token = auth_client

    res = client.post('/api/auth/refresh')
    access = res.json['access_token']

    assert res.status_code == 200 and access


def test_guarded_logout(client):
    '''
        Tests that the logout endpoint is guarded.
    '''
    # No bearer token is passed
    res = client.post('/api/auth/logout')

    assert res.status_code == 401


def test_logout(auth_client):
    '''
        Tests that the logout endpoint works.
    '''
    client, access_token = auth_client

    res = client.post('/api/auth/logout', headers={'Authorization': access_token})

    # test that a guarded route no longer works with either the access or refresh token
    res1 = client.post('/api/auth/logout', headers={'Authorization': access_token})
    res2 = client.post('/api/auth/refresh')

    assert res.status_code == 200 and res1.status_code == 401 and res2.status_code == 401
