import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    dynamoDB = boto3.resource('dynamodb')
    table = dynamoDB.Table('Analytics')
    
    get = json.loads(event['body'])
    response = table.get_item(
        Key = {
            'gamename':get['gamename']
        }
    )
    now = datetime.now()
    t = int(now.strftime("%Y%m%d%H%M%S"))

    print(t)
    try:
        item = response['Item']
    except:
        response = table.put_item(
            Item = {
                'gamename':get['gamename'],
                get['username']:{get['eventname']:[t]}
            }
        )
        item = 'SUCCESSS'
    else:
        temp = get['username'] +  "." + get['eventname']
        try:
            eName = item[get['username']][get['eventname']]
        except:
            response = table.update_item(
                Key={
                    'gamename':get['gamename']
                },
                UpdateExpression="set "+ temp + "= :i", 
                ExpressionAttributeValues={
                    ':i': [t],
                },
                ReturnValues="UPDATED_NEW"    
            )
            item = 'UPDATED'
        else:
            response = table.update_item(
                Key={
                    'gamename':get['gamename']
                },
                UpdateExpression="set "+ temp + " = list_append(" + temp + ", :i)", 
                ExpressionAttributeValues={
                    ':i': [t],
                },
                ReturnValues="UPDATED_NEW"    
            )
            item = 'UPDATED'
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
