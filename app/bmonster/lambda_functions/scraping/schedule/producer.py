import json
import os
import uuid

import boto3

from .consumer import main as consumer


STUDIO_LIST = {
    "GINZA": "0001",
    "AOYAMA": "0002",
    "EBISU": "0003",
    "SHINJUKU": "0004",
    "IKEBUKURO": "0006",
    "SHIBUYA": "0010",
}


def main():
    for studio_name, studio_code in STUDIO_LIST.items():
        message = {"studio_code": studio_code, "studio_name": studio_name}
        if os.environ["STAGE"] == "local":
            consumer(**message)
        else:
            client = boto3.client("sqs", region_name="ap-northeast-1")
            client.send_message(
                QueueUrl=os.environ["SCRAPING_QUEUE_URL"],
                MessageGroupId=str(uuid.uuid4()),
                MessageBody=json.dumps(message),
            )


def lambda_handler(event, context):
    main()
    return {
        "statusCode": 200,
        "body": "success",
    }
