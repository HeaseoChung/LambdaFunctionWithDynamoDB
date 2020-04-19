import json
import boto3

def lambda_handler(event, context):
    dynamoDB = boto3.resource('dynamodb')
    table = dynamoDB.Table('RemoteSettingManagement')
    
    get = json.loads(event['body'])
    response = table.get_item(
        Key = {
            'gamename':get['gamename']
        }
    )
    
    try:
        item = response['Item']
    except:
        item = 'FAILURE'
    else:
        try:
            response = table.update_item(
                Key = {
                    'gamename':get['gamename']
                },
                UpdateExpression="set field." + get['variableName'] + " = :v",
                ExpressionAttributeValues={
                    ':v':get['valueName']
                },
                ReturnValues="UPDATED_NEW"
            )
        except:
            item = 'FAILURE2'
        else:
            item = 'SUCCESS'
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
