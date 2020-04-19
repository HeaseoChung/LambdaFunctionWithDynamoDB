import json
import boto3

def lambda_handler(event, context):
    dynamoDB = boto3.resource('dynamodb')
    table = dynamoDB.Table('user')
        
    get = json.loads(event['body'])
    response = table.get_item(
        Key = {
            'id':get['id']
        }
    )

    try:
        item = response['Item']
    except:
        item = 'FAILURE'
    else:
        if((item['cookie'] != get['cookie']) | (item['cookie'] == "NONE")):
            item = 'FAILURE'
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
