import json
import utils.response as res
from config import dynamodb

def handler(event, context):

    # Get User from DynamoDB.
    database_response = dynamodb.get_item(
        TableName="Users",
        Key={
            'Identifier': {
                'S': '4280fa00-0f1a-41a3-8b64-fbea67238ea4'
            }
        }
    )

    print(database_response)
    return res.build(200, database_response)
