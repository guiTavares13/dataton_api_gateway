import boto3
import json
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION = os.getenv('AWS_REGION')
LAMBDA_FUNCTION_NAME = os.getenv('LAMBDA_FUNCTION_NAME')
ENDPOINT_URL = os.getenv('ENDPOINT_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
    endpoint_url=ENDPOINT_URL  # Use o endpoint do .env
)

def invoke_lambda(payload):
    response = lambda_client.invoke(
        FunctionName=LAMBDA_FUNCTION_NAME,
        InvocationType='RequestResponse',
        Payload=payload.encode('utf-8')
    )
    return response['Payload'].read().decode('utf-8')