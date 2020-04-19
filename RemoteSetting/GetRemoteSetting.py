import json
import boto3
import decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
        
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
        item = "FAILURE"
        
    return {
        'statusCode': 200,
        'body': json.dumps(item, indent=4, cls=DecimalEncoder)
    }
