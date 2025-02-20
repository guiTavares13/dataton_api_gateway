import jwt
import datetime
from flask import request, jsonify
from functools import wraps
from werkzeug.security import check_password_hash
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, SECRET_KEY, ENDPOINT_URL
import boto3

dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION, endpoint_url=ENDPOINT_URL)
table = dynamodb.Table('dataton-admins')

# Função de login com JWT
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


# Função para gerar JWT
def generate_jwt(user_id):
    payload = {
        'sub': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Token expira em 1 hora
        'iat': datetime.datetime.utcnow()  # Data de emissão
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Função de login
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

        # Obter o token da cabeçalho da requisição
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            # Decodificar o token
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = payload['sub']  # ID do usuário presente no payload
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated_function
