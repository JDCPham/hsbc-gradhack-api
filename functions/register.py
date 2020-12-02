import json
import utils.response as res
from config import dynamodb

def handler(event, context):
    try:
        # Get input from user.
        body = json.loads(event.get('body'))

        # Get Email, First Name, Last Name, and Password.
        email = body.get('email')
        first_name = body.get('first_name')
        last_name = body.get('last_name')
        password = body.get('password')

        # Get response from database.
        response = dynamodb.get_item(
            TableName="Users",
            Key={ 'Email': { 'S': email } }
        ).get("Item", None)

        # check if already registered
        if (response is not None): 
            return res.build(400, {
                'registered': False,
                'message': 'email existed'
            })

        # update user db
        dynamodb.put_item(
            TableName="Users",
            Item={
                'Email': {'S': email},
                'Balance': {'N': '0'},
                'First Name': {'S': first_name},
                'Last Name': {'S': last_name},
                'Password': {'S': password}
            }
        )

        # update upcoming activity db
        dynamodb.put_item(
            TableName="Upcoming-Activities",
            Item={
                'Email': {'S': email},
                'Activities': {'S': '[]'}
            }
        )

        # update transcation db
        dynamodb.put_item(
            TableName="Transactions",
            Item={
                'Email': {'S': email},
                'Transactions': {'S': '[]'}
            }
        )

        return res.build(200, {
            'registered': True,
            'message': "Have registered"
        })

    except Exception as e:

        print(str(e))

        return res.build(400, {
            'registered': False,
            'message': str(e)
        })