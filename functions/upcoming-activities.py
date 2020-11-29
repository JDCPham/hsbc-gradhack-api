import json
import utils.response as res
from config import dynamodb
import arrow

def handler(event, context):

    try:

        # Get input from user.
        path_parameters = event.get('pathParameters')

        # Email
        email = path_parameters.get('email')

        # Check if Null.
        if (email is None): raise Exception("Email not found.")

         # Get response from database.
        response = dynamodb.get_item(
            TableName="Upcoming-Activities",
            Key={ 'Email': { 'S': email } }
        ).get("Item", {})

        # Get Activities
        activities = json.loads(response.get('Activities', {}).get('S'))

        # Check if none
        if (activities is None): activities = []

        # Create empty list to store results
        upcoming_activities = []

        # Loop over activities
        for activity in activities:
            # Convert timestamps
            arrow_activity_timestamp = arrow.get(activity['timestamp'])
            arrow_current_timestamp = arrow.utcnow()
            diff = arrow_activity_timestamp - arrow_current_timestamp
            days = diff.days 

            if (days < 0):
                print("Did not add the following activity:")
                print(activity)
            else:
                upcoming_activities.append(activity['identifier'])

        # Get activity detail
        results = get_activity_detail(upcoming_activities)

        return res.build(200, results)

    except Exception as e:

        print(str(e))

        return res.build(400, [])


def get_activity_detail(activities=[]):

    results = []

    for activity in activities:

        try:

            # Get response from database.
            response = dynamodb.get_item(
                TableName="Activities",
                Key={ 'Identifier': { 'S': activity } }
            ).get("Item", {})

            # Append to return object
            results.append({
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
            })

            print(response)
        except Exception as e:

            print(e)

    return results

        

