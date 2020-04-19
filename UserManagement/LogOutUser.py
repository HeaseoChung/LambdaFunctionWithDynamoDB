import json
import boto3
def lambda_handler(event, context):
    dynamoDB = boto3.resource('dynamodb')
    table = dynamoDB.Table('user')
        
    get = json.loads(event['body'])
    id = table.get_item(
        Key = {
            'id':get['id']
        }
    )
    
    try:
        item = id['Item']
    except:
        item = 'FAILURE'
    else:
        if((item['cookie'] != get['cookie']) | (item['cookie'] == 'NONE')):
            item = 'FAILURE'
        else:
            response = table.update_item(
                Key = {
                    'id':get['id']
                },
                UpdateExpression="set cookie = :c",
                ExpressionAttributeValues = {
                    ':c':"NONE"
                },
                ReturnValues="UPDATED_NEW"
            )
            item = 'SUCCESS'
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
