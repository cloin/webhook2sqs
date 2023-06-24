import os
import json
import boto3
import logging

# Retrieve the SQS Queue URL and AWS Region name from the environment variables
QUEUE_URL = os.getenv('QUEUE_URL')
REGION_NAME = os.getenv('REGION_NAME')

# Setup the logging. By default, the logging level is set to INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize an SQS client object using the boto3 library
sqs = boto3.client('sqs', region_name=REGION_NAME)

def lambda_handler(event, context):
    # Parse the 'body' from the incoming event. If it doesn't exist, use an empty dictionary
    body = json.loads(event.get('body', '{}'))

    # Retrieve the 'headers' from the incoming event. If it doesn't exist, use an empty dictionary
    headers = event.get('headers', {})

    # Construct the message that will be sent to SQS
    message = {
        'body': body,
        'headers': headers
    }
    
    # Log the message that will be sent to SQS
    logger.info(f"Sending event: {json.dumps(message)}")

    # Send the constructed message to the SQS Queue
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message)
    )

    # Print the MessageID of the sent message for debugging purposes
    print(f"Message sent to SQS! MessageID is {response['MessageId']}")

    # Return a response indicating success, including the MessageID in the body
    return {
        'statusCode': 200,
        'body': f"Message sent to SQS! MessageID is {response['MessageId']}"
    }
