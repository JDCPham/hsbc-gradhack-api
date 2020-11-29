# Import Modules
import boto3

# Clients
session = boto3.Session()
dynamodb = session.client('dynamodb')
