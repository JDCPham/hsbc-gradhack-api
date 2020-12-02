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
            TableName="Transactions",
            Key={ 'Email': { 'S': email } }
        ).get("Item", {})
       
        if (response is None): return res.build(200, [])

        transactions = json.loads(response.get("Transactions", {}).get('S', "[]"))

        return res.build(200, transactions)
       
    except Exception as e:

        print(str(e))

        return res.build(400, {})

