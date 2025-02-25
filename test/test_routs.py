import json
from src.api.auth import generate_jwt

def test_invoke_lambda_route(client, mocker):
    mocker.patch('src.api.lambda_client.invoke_lambda', return_value={
        'statusCode': 200,
        'body': {'message': 'success'}
    })

    token = generate_jwt('admin')

    response = client.post('/api/invoke-lambda', json={
        'userId': 'admin'
    }, headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'response' in data
    assert data['response']['statusCode'] == 200
    assert data['response']['body']['message'] == 'success'