import boto3
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION

dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)

def get_item_from_dynamodb(table_name, key):
    """
    Recupera um item de uma tabela DynamoDB.
    :param table_name: O nome da tabela.
    :param key: A chave para o item a ser recuperado.
    :return: O item encontrado ou None.
    """
    table = dynamodb.Table(table_name)
    response = table.get_item(Key=key)
    return response.get('Item')