import boto3
from src.config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, ENDPOINT_URL

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
    endpoint_url=ENDPOINT_URL
)

table = dynamodb.Table('dataton-admins')

response = table.scan()
print("Itens na tabela 'dataton-admins':")
for item in response.get('Items', []):
    print(item)

if not response.get('Items'):
    print("Tabela está vazia!")
