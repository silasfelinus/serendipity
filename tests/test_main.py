def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the application!" in response.data