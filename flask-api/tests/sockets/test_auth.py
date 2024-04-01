from tests.helpers import sio


def test_invalid_auth(sio_client):
    """
        Tests that the client can't access SocketIO without credentials.
    """
    assert not sio_client.is_connected()

def test_valid_auth(auth_sio_client):
    """
        Tests that the client can access SocketIO with the correct credentials.
    """
    assert auth_sio_client.is_connected()
