import boto3
from werkzeug.security import generate_password_hash
from src.config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION

# Inicializa o cliente DynamoDB com as credenciais e endpoint para o LocalStack
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id="test",  # Credenciais do LocalStack
    aws_secret_access_key="test",  # Credenciais do LocalStack
    region_name="sa-east-1",  # Ou a região que você estiver utilizando
    endpoint_url="http://127.0.0.1:4566"  # LocalStack
)

table = dynamodb.Table('dataton-admins')  # A tabela correta

# Verifique a resposta da requisição
try:
    response = table.get_item(Key={'id': 'admin'})
    print(response)
except Exception as e:
    print(f"Erro ao acessar o DynamoDB: {str(e)}")
