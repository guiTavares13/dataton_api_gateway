import boto3
import jwt
import datetime
from flask import request, jsonify, current_app
from functools import wraps
from werkzeug.security import check_password_hash
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, SECRET_KEY, ENDPOINT_URL

# Configurar o cliente DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
    endpoint_url=ENDPOINT_URL
)
table = dynamodb.Table('dataton-admins')

def login_user(username, password):
    response = table.get_item(Key={'id': username})
    print(f"Response do DynamoDB para {username}: {response}")

    if 'Item' not in response:
        print(f"Usuário {username} não encontrado.")
        return None

    stored_password = response['Item']['password']
    print(f"Senha armazenada (hash): {stored_password}")

    if check_password_hash(stored_password, password):
        print("Senha válida!")
        return response['Item']

    print("Senha inválida!")
    return None

def generate_jwt(user_id):
    payload = {
        'sub': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def login_route():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = login_user(username, password)
    if user:
        token = generate_jwt(user['username'])
        return jsonify({"message": "Login successful", "token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        if current_app.config.get("TESTING"):  # Se estiver rodando testes, pula autenticação
            return f(*args, **kwargs)

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = payload['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated_function