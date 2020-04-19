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
    table = dynamoDB.Table('Analytics')
    
    get = json.loads(event['body'])
    response = table.get_item(
        Key = {
            'gamename':get['gamename']
        }
    )
    result = {'time':[], 'count': 0}
    try:
        item = response['Item']
    except:
        item = 'FAILURE'
    else:
        #temp = get['username'] + "." + get['eventname']
        startTime = get['starttime']
        endTime = get['endtime'] 
        eventList = item[get['username']][get['eventname']]
        print(eventList)
        for e in eventList:
            if((startTime < e) & (e < endTime)):
                result['time'].append(e)
                result['count']+=1
            #FilterExpression=Attr(temp).between(get['starttime'], get['endtime'])
    return {
        'statusCode': 200,
        'body': json.dumps(result, indent=4, cls=DecimalEncoder)
    }
