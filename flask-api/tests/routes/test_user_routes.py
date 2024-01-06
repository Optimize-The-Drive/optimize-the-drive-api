'''
    Defines user route tests
'''


def test_example_route(client):
    '''
        Tests the example route
    '''
    response = client.get(
        '/api/user/example',
    )

    assert response.status_code == 200
