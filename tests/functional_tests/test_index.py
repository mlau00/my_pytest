def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {'hello': 'world'}
