import json
import boto3
import random
import string

def randomString(stringLength=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))
    
def lambda_handler(event, context):
    dynamoDB = boto3.resource('dynamodb')
    table = dynamoDB.Table('user')
        
    get = json.loads(event['body'])
    result = {}
    result['cookie'] = "NONE"
    result['result'] = "NONE"
    
    cookie = randomString()
    
    account = table.get_item(
        Key = {
            'id':get['id'],
        }    
    )
    item = account['Item']
    
    if(item['password'] == get['password']):
        response = table.update_item(
            Key = {
                'id':get['id']
            },
            UpdateExpression="Set cookie = :c",
            ExpressionAttributeValues = {
                ':c':cookie
            },
            ReturnValues="UPDATED_NEW"
        )
        result['result'] = 'SUCCESS'
        result['cookie'] = cookie
        result['id'] = get['id']
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    else:
        item = 'FAILURE'
        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }