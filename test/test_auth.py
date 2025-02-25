import json
from src.api.auth import generate_jwt

def test_login_success(client, mocker):
    # Mock the DynamoDB response
    mocker.patch('src.api.auth.table.get_item', return_value={
        'Item': {
            'id': 'admin',
            'password': 'pbkdf2:sha256:150000$abc$1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef'
        }
    })
    # Mock the password check
    mocker.patch('src.api.auth.check_password_hash', return_value=True)

    response = client.post('/api/login', json={
        'username': 'admin',
        'password': 'senha'
    })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data

def test_login_failure(client, mocker):
    # Mock the DynamoDB response
    mocker.patch('src.api.auth.table.get_item', return_value={})

    response = client.post('/api/login', json={
        'username': 'admin',
        'password': 'senha'
    })

    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['message'] == 'Invalid credentials'