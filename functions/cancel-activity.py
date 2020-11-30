import json
import utils.response as res
from config import dynamodb
import arrow

def handler(event, context):

    try:

        # Get input from user.
        path_parameters = event.get('pathParameters')

        # Activity identifier
        activity = path_parameters.get('activityId')
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
        new_activities = []
        activities = json.loads(activity_response.get("Activities", {}).get('S', {}))

        for a in activities:
            print(a)
            if (a['identifier'] != activity): new_activities.append(a)


        user_response = dynamodb.get_item(
            TableName="Users",
            Key={ 'Email': {'S': email}}
        ).get("Item", {})

        if (user_response is None): raise Exception("Could not find user.")

        balance = user_response.get('Balance', {}).get('N', 0)

        dynamodb.update_item(
            TableName="Users",
            Key={'Email': {'S': email } },
            UpdateExpression='SET #balance = :balanceVal',
            ExpressionAttributeNames={'#balance': "Balance"},
            ExpressionAttributeValues={":balanceVal": {'N': str(float(balance) - 5)}}
        )

        dynamodb.put_item(
            TableName="Upcoming-Activities",
            Item={
                'Email': {'S': email},
                'Activities': {'S': json.dumps(new_activities)}
            }
        )

        dynamodb.put_item(
            TableName="Transactions",
            Item={
                'Email': {'S': email},
                'Transactions': {'S': json.dumps({
                    'amount': -5,
                    'reason': "Cancelled Activity",
                    'timestamp': '{}T{}Z'.format(arrow.utcnow().format("YYYY-MM-DD"), arrow.utcnow().format("HH:mm:ss"))
                })}
            }
        )

        return res.build(200, {
            'deleted': True
        })
       
    except Exception as e:

        print(str(e))

        return res.build(400, {})

