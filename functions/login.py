import json
import utils.response as res
from config import dynamodb

def handler(event, context):
    return res.build(200, {})
