import json

def build(code, body):
    return {
        'statusCode': code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
        },
        'body': json.dumps(body)
    }