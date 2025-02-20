import boto3
from werkzeug.security import generate_password_hash
from src.config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION

# Inicializa o cliente DynamoDB com credenciais e região fornecidas
dynamodb = boto3.resource('dynamodb', 
                          aws_access_key_id='test',
                          aws_secret_access_key='test',
                          region_name='sa-east-1',
                          endpoint_url="http://127.0.0.1:4566")


# Nome da tabela onde vamos inserir os dados
table = dynamodb.Table('dataton-admins')  # A tabela de admins criada no LocalStack

# Lista de usuários a serem inseridos
users_to_insert = [
    {'user': 'admin', 'password': 'senha'},
    {'user': 'guilherme', 'password': 'senha'},
    {'user': 'lucas', 'password': 'senha'},
    {'user': 'yago', 'password': 'senha'}
]

# Função para inserir os usuários na tabela
def insert_users():
    for user in users_to_insert:
        # Gera o hash da senha para armazenar de forma segura
        hashed_password = generate_password_hash(user['password'])
        
        # Inserir o item no DynamoDB
        response = table.put_item(
            Item={
                'id': user['user'],  # Usando o nome do usuário como o 'id'
                'username': user['user'],
                'password': hashed_password
            }
        )
        print(f"Usuário {user['user']} inserido com sucesso.")
        print(response)

# Chama a função para inserir os usuários
if __name__ == "__main__":
    insert_users()
