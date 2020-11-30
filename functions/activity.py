import json
import utils.response as res
from config import dynamodb

def handler(event, context):

    try:

        # Get input from user.
        path_parameters = event.get('pathParameters')

        # Activity
        activity = path_parameters.get('activity')

        # Check if Null.
        if (activity is None): raise Exception("Activity not found.")

         # Get response from database.
        response = dynamodb.get_item(
            TableName="Activities",
            Key={ 'Identifier': { 'S': activity } }
        ).get("Item")

        # Check item exists
        if (response is None): raise Exception("Activity not found.")


        # Build Response Object
        response = {
            'Identifier': activity,
                'Cost': response.get('Cost', {}).get('N'),
                'Description': response.get('Description', {}).get('S'),
                'Host': response.get('Host', {}).get('S'),
                'Image': response.get('Image', {}).get('S'),
                'Location': response.get('Location', {}).get('S'),
                'Name': response.get('Name', {}).get('S'),
                'Virtual': response.get('Virtual', {}).get('BOOL'),
                'Timestamp': response.get('Timestamp', {}).get('S'),
                'Penalty': response.get('Penalty', {}).get('N'),
                'Postcode': response.get('Postcode', {}).get('S'),
                'Latitude': response.get('Latitude', {}).get('N'),
                'Longitude': response.get('Longitude', {}).get('N')
        }

        return res.build(200, response)
       
    except Exception as e:

        print(str(e))

        return res.build(400, None)

