# pylint: disable=C0114

def test_crud(client): # pylint: disable=C0116
    response = client.get('/state')
    assert response.status_code == 404

    data1 = "DATA1".encode('utf-8')
    response = client.post('/state', data=data1)
    assert response.status_code == 200
    response = client.get('/state')
    assert response.status_code == 200
    assert response.data == data1

    data2 = "DATA2".encode('utf-8')
    response = client.post('/state', data=data2)
    assert response.status_code == 200
    response = client.get('/state')
    assert response.status_code == 200
    assert response.data == data2

    response = client.delete('/state')
    assert response.status_code == 200

    response = client.get('/state')
    assert response.status_code == 404

def test_lock(client): # pylint: disable=C0116
    response = client.open('/state', method='UNLOCK')
    assert response.status_code == 404

    response = client.open('/state', method='LOCK')
    assert response.status_code == 200
    response = client.open('/state', method='LOCK')
    assert response.status_code == 409

    response = client.open('/state', method='UNLOCK')
    assert response.status_code == 200

    response = client.open('/state', method='UNLOCK')
    assert response.status_code == 404

def test_auth(client): # pylint: disable=C0116
    response = client.get('/state')
    assert response.status_code != 401

    response = client.get('/state', credentials='wrong-data')
    assert response.status_code == 401

    response = client.get('/state', disable_auth=True)
    assert response.status_code == 401
