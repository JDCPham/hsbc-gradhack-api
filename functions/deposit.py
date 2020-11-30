import json
import utils.response as res
from config import dynamodb
import arrow

def handler(event, context):

    try:

        # Get input from user.
        path_parameters = event.get('pathParameters')

        # Email and Amount
        amount = path_parameters.get('amount', 0)
        email = path_parameters.get('email')

        # Check if Null.
        if (email is None): raise Exception("Email not found.")

        # Get Current Balance
        preBalance = float(dynamodb.get_item(
            TableName="Users",
            Key={ 'Email': { 'S': email } }
        ).get("Item", {}).get("Balance", {}).get("N", 0))

        # Update Item
        dynamodb.update_item(
            TableName="Users",
            Key={'Email': {'S': email } },
            UpdateExpression='SET #balance = :balanceVal',
            ExpressionAttributeNames={'#balance': "Balance"},
            ExpressionAttributeValues={":balanceVal": {'N': str(preBalance + float(amount))}}
        )

        # Get Transactions
        transactions = json.loads(dynamodb.get_item(
            TableName="Transactions",
            Key={ 'Email': { 'S': email } }
        ).get("Item", {}).get("Transactions", {}).get("S", "[]"))

        transactions.append({
            'amount': amount,
            'reason': "Deposit from debit card",
            'timestamp': '{}T{}Z'.format(arrow.utcnow().format("YYYY-MM-DD"), arrow.utcnow().format("HH:mm:ss"))
        })

        # Update Item
        dynamodb.update_item(
            TableName="Transactions",
            Key={'Email': {'S': email } },
            UpdateExpression='SET #transactions = :transactionsVal',
            ExpressionAttributeNames={'#transactions': "Transactions"},
            ExpressionAttributeValues={":transactionsVal": {'S': json.dumps(transactions)}}
        )
   
        # Get Current Balance
        postBalance = float(dynamodb.get_item(
            TableName="Users",
            Key={ 'Email': { 'S': email } }
        ).get("Item", {}).get("Balance", {}).get("N", 0))

        return res.build(200, {
            "balanceBefore": preBalance,
            "balanceAfter": postBalance
        })
       
    except Exception as e:

        print(str(e))

        return res.build(400, {
            'error': str(e)
        })

