import boto3
import json
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, LAMBDA_FUNCTION_NAME, ENDPOINT_URL

lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
    endpoint_url=ENDPOINT_URL
)

def invoke_lambda(payload):
    response = lambda_client.invoke(
        FunctionName=LAMBDA_FUNCTION_NAME,
        InvocationType='RequestResponse',
        Payload=payload.encode('utf-8')
    )
    return response['Payload'].read().decode('utf-8')
