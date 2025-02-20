import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

AWS_REGION = os.getenv('AWS_REGION', 'sa-east-1')
DYNAMODB_TABLE = os.getenv('DYNAMODB_TABLE', 'users')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
ENDPOINT_URL = os.getenv('ENDPOINT_URL')

LAMBDA_FUNCTION_NAME = os.getenv('LAMBDA_FUNCTION_NAME', 'hello-world-lambda')

SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key') 
