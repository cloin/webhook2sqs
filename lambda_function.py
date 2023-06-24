import os
import json
import boto3
import logging

# In lamda, set these in the Configuration tab
QUEUE_URL = os.getenv('QUEUE_URL')
REGION_NAME = os.getenv('REGION_NAME')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sqs = boto3.client('sqs', region_name=REGION_NAME)

def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))
    headers = event.get('headers', {})

    message = {
        'body': body,
        'headers': headers
    }
    
    logger.info(f"Sending event: {json.dumps(message)}")

    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message)
    )

    print(f"Message sent to SQS! MessageID is {response['MessageId']}")

    return {
        'statusCode': 200,
        'body': f"Message sent to SQS! MessageID is {response['MessageId']}"
    }
