import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from ....models import Schedule
from ....scraping_functions import scraping_schedule_by_studio


def main(studio_name: str, studio_code: str):
    for item in scraping_schedule_by_studio(studio_name, studio_code):
        with Schedule.batch_write() as batch:
            batch.save(
                Schedule(
                    **item.model_dump(),
                    ttl=datetime.now(tz=ZoneInfo("Asia/Tokyo")) + timedelta(days=1)
                )
            )


def lambda_handler(event, context):
    record = event["Records"][0]
    body = json.loads(record["body"])
    main(body["studio_name"], body["studio_code"])
    return {
        "statusCode": 200,
        "body": "success",
    }
