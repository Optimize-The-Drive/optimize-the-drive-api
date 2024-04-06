"""Defines trip route tests"""

import pytest
from tests.helpers import get_response_body, trip_repo


def test_trip_guarded(client):
    """
        Tests that the trip endpoints are guarded.

        POST /api/trip/
        PATCH /api/trip/<id>
        DELETE /api/trip/<id>
    """
    res = client.post('/api/trip/', json={"name": "test", "description": "shouldn't work"})
    res1 = client.patch('/api/trip/1', json={"name": "test", "description": "shouldn't work"})
    res2 = client.delete('/api/trip/1')

    assert res.status_code == 401
    assert res1.status_code == 401
    assert res2.status_code == 401


def test_trip_not_found(auth_client):
    """
        Tests that the route returns not found if calling test routes.

        PATCH /api/trip/<id>
        GET /api/trip/<id>
    """
    client, headers = auth_client("tripEditUser1", "Password1!")

    not_found = client.patch(
        "/api/trip/11111111111",
        json={"name": "asdf"},
        headers={'Authorization': headers['Authorization']}
    )

    not_found1 = client.delete(
        "/api/trip/11111111111",
        headers={'Authorization': headers['Authorization']}
    )

    assert not_found.status_code == 404
    assert not_found1.status_code == 404


def test_trip_forbidden(auth_client):
    """
        Tests that a user can't modify or delete a trip that doesn't belong to them.
        
        PATCH /api/trip/<id> 
    """
    client, headers = auth_client("tripEditUser1", "Password1!")
    trip = {
        "name": "trip", "description": ""
    }

    res = client.post(
        '/api/trip/',
        json=trip,
        headers={'Authorization': headers['Authorization']}
    )
    trip_id = get_response_body(res)["trip"]["id"]

    # Login as a different user and try to edit the above trip
    client1, headers1 = auth_client("tripEditUser2", "Password1!")

    trip_edit = {
        "name": "not allowed",
        "description": "not allowed"
    }

    forbidden_res = client1.patch(
        f"/api/trip/{trip_id}",
        json=trip_edit,
        headers={'Authorization': headers1['Authorization']}
    )

    forbidden_res1 = client1.delete(
        f"/api/trip/{trip_id}",
        headers={'Authorization': headers1['Authorization']}
    )

    assert forbidden_res.status_code == 403
    assert forbidden_res1.status_code == 403


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

    res = client.post(
        '/api/trip/',
        headers={'Authorization': headers['Authorization']}, json=example_trip
    )
    res_route = get_response_body(res)["trip"]

    assert res.status_code == 201
    assert res_route["name"] == example_trip["name"]
    assert res_route["description"] == example_trip["description"]


def test_trip_create_validation(auth_client):
    """
        Tests that the trip create route validation works.
        
        POST /api/trip
    """

    client, headers = auth_client()

    # Tests that name of zero length fails validation
    example_trip = {
        "name": "",
        "description": "fdsa"
    }

    res = client.post(
        '/api/trip/',
        headers={'Authorization': headers['Authorization']}, json=example_trip
    )

    assert res.status_code == 422

    # Tests that name of large length fails validation
    example_trip = {
        "name": "".join("a" for i in range(512)),
        "description": "fdsa"
    }

    res = client.post(
        '/api/trip/',
        headers={'Authorization': headers['Authorization']}, json=example_trip
    )

    assert res.status_code == 422

    # Tests that description of large length fails validation
    example_trip = {
        "name": "fdas",
        "description": "".join("a" for i in range(1024))
    }

    res = client.post(
        '/api/trip/',
        headers={'Authorization': headers['Authorization']}, json=example_trip
    )

    assert res.status_code == 422

     # Tests that no description passed is valid
    example_trip = {
        "name": "fdas",
    }

    res = client.post(
        '/api/trip/',
        headers={'Authorization': headers['Authorization']}, json=example_trip
    )

    assert res.status_code == 201


def test_trip_edit(auth_client):
    """
        Tests that the trip edit route works.

        PATCH /api/trip/<id>
    """

    client, headers = auth_client("tripEditUser1", "Password1!")
    original_trip = {
        "name": "trip", "description": ""
    }

    res = client.post(
        '/api/trip/',
        json=original_trip,
        headers={'Authorization': headers['Authorization']}
    )
    original_trip_id = get_response_body(res)["trip"]["id"]

    updated_trip = {
        "name": "trip name updated!", "description": "A description now!"
    }

    res_patch = client.patch(
        f'/api/trip/{original_trip_id}',
        json=updated_trip,
        headers={'Authorization': headers['Authorization']}
    )
    updated_trip_res = get_response_body(res_patch)["trip"]

    assert res_patch.status_code == 200
    assert updated_trip["name"] == updated_trip_res["name"]
    assert updated_trip['description'] == updated_trip_res['description']


@pytest.mark.usefixtures("app_ctx")
def test_delete_trip(auth_client):
    """
        Tests that the delete trip works correctly
        
        DELETE /api/trip/<id>
    """
    client, headers = auth_client("tripDelete1", "Password1!")

    trip = {
        "name": "trip", "description": ""
    }

    res = client.post(
        '/api/trip/',
        json=trip,
        headers={'Authorization': headers['Authorization']}
    )
    trip_id = get_response_body(res)["trip"]["id"]

    res = client.delete(
        f"/api/trip/{trip_id}",
        headers={'Authorization': headers['Authorization']}
    )

    trip = trip_repo.by_id(trip_id)

    assert res.status_code == 200 
    assert trip is None
