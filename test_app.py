import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b'my-app' in res.data

def test_health(client):
    res = client.get('/health')
    assert res.status_code == 200
    assert b'healthy' in res.data

def test_add(client):
    res = client.get('/add/5/3')
    assert res.status_code == 200
    assert b'8' in res.data
