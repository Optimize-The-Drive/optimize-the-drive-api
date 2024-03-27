"""Defines trip route tests"""

from tests.helpers import get_response_body

def test_trip_create_guarded(client):
    """
        Tests that the trip create route is protected.

        POST /api/trip/
    """

    res = client.post('/api/trip/', json={"name": "test", "description": "shouldn't work"})

    assert res.status_code == 401
    
def test_trip_create(auth_client):
    """
        Tests that the trip create route works.
        
        POST /api/trip
    """

    client, headers = auth_client()

    example_trip = {
        "name": "trip_one",
        "description": "this is trip_one's description"
    }

    res = client.post('/api/trip/', headers={'Authorization': headers['Authorization']}, json=example_trip)
    res_route = get_response_body(res)

    assert res.status_code == 201
