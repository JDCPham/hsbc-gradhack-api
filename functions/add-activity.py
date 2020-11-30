import json
import utils.response as res
from config import dynamodb
import arrow

def handler(event, context):

    try:

        # Get input from user.
        path_parameters = event.get('pathParameters')

        # Activity identifier
        activity = path_parameters.get('id')
        email = path_parameters.get('email')

        # Check if Null.
        if (activity is None): raise Exception("Activity not found.")
        if (email is None): raise Exception("Email not found.")

         # Get response from database.
        activity_response = dynamodb.get_item(
            TableName="Upcoming-Activities",
            Key={ 'Email': { 'S': email} }
        ).get("Item", {})

        if (activity_response is None): raise Exception("Could not find activity.")

        # Get Activities
        activities = json.loads(activity_response.get("Activities", {}).get('S', {}))

        # Check if exists already
        for a in activities:
            print(a.get('identifier'))
            if (a.get('identifier') == activity): raise Exception("Activity already exists in user profile.")

        # Get response from database.
        response = dynamodb.get_item(
            TableName="Activities",
            Key={ 'Identifier': { 'S': activity } }
        ).get("Item")

        timestamp = response.get('Timestamp', {}).get('S')

        # Check item exists
        if (response is None): raise Exception("Activity not found.")

        before_count = len(activities)

        # Add Activity
        activities.append({
            'identifier': activity,
            'timestamp': timestamp
        })

        after_count = len(activities)

        dynamodb.put_item(
            TableName="Upcoming-Activities",
            Item={
                'Email': {'S': email},
                'Activities': {'S': json.dumps(activities)}
            }
        )


        return res.build(200, {
            'added': True,
            'before': before_count,
            'after': after_count
        })
       
    except Exception as e:

        print(str(e))

        return res.build(400, {
            'error': str(e),
            'added': False
        })

