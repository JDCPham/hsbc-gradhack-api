import json
import utils.response as res
from config import dynamodb

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
            TableName="Users",
            Key={ 'Email': { 'S': email } }
        ).get("Item", {})

        # Build Response Object
        response = {
            'email': response.get('Email', {}).get('S'),
            'balance': response.get('Balance', {}).get('N'),
            'firstName': response.get('First Name', {}).get('S'),
            'lastName': response.get('Last Name', {}).get('S')
        }

        return res.build(200, response)
       
    except Exception as e:

        print(str(e))

        return res.build(400, {})

