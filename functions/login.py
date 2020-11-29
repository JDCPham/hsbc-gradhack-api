import json
import utils.response as res
from config import dynamodb

def handler(event, context):

    try:

        # Get input from user.
        body = json.loads(event.get('body'))

        # Get Email and Password.
        email = body.get('email')
        password = body.get('password')

        # Get response from database.
        response = dynamodb.get_item(
            TableName="Users",
            Key={ 'Email': { 'S': email } }
        ).get("Item", {})

        # Get password from database response.
        database_password = response.get('Password', {}).get('S')

        # Compare Password
        if (password == database_password):
            return res.build(200, { 
                'loggedIn': True,
                'message': "Logged in"
            })
        else:
            return res.build(400, {
                'loggedIn': False,
                'message': "Wrong password"
            })


    except Exception as e:

        print(str(e))

        return res.build(400, {
            'loggedIn': False,
            'message': str(e)
        })

