import json
import utils.response as res
from config import dynamodb
import arrow

def handler(event, context):

    try:

        response = dynamodb.scan(
            TableName='Activities',
            AttributesToGet=['Identifier', 'Name', 'Cost', 'Timestamp', 'Virtual', 'Location', 'Host', 'Image']
        ).get('Items')

        results = []

        for activity in response:
            results.append({
                'Name': activity.get('Name', {}).get('S'),
                'Timestamp': activity.get('Timestamp', {}).get('S'),
                'Cost': activity.get('Cost', {}).get('N'),
                'Identifier': activity.get('Identifier', {}).get('S'),
                'Virtual': activity.get('Virtual', {}).get('BOOL'),
                'Location': activity.get('Location', {}).get('S'),
                'Host': activity.get('Host', {}).get('S'),
                'Image': activity.get('Image', {}).get('S')
            })

        return res.build(200, results)
       
    except Exception as e:

        print(str(e))

        return res.build(400, {
            'error': str(e)
        })

