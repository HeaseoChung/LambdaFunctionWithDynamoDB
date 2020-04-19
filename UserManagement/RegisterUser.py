import json
import boto3
def lambda_handler(event, context):
    dynamoDB = boto3.resource('dynamodb')
    table = dynamoDB.Table('user')
        
    get = json.loads(event['body'])
    id = table.get_item(
        Key = {
            'id':get['id'],
        }    
    )
    try:
        item = id['Item']
    except:
        response = table.put_item(
           Item = {
                'id':get['id'],
                'password':get['password'],
                'email':get['email'],
                'cookie':"NONE"
            }    
        )
        item = "SUCCESS"
    else:
        item = "FAILURE"
        
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
