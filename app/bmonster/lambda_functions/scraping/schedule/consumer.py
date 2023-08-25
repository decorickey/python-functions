import json
from collections import defaultdict
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from ....models import Performer, Schedule
from ....scraping_functions import scraping_schedule_by_studio


def main(studio_name: str, studio_code: str):
    programs_by_performer: defaultdict[str, set[str]] = defaultdict(set)
    with Schedule.batch_write() as batch:
        for item in scraping_schedule_by_studio(studio_name, studio_code):
            programs_by_performer[item.performer_name].add(item.program)
            props = item.model_dump()
            props.pop("url")
            batch.save(
                Schedule(
                    **props,
                    ttl=datetime.now(tz=ZoneInfo("Asia/Tokyo")) + timedelta(days=1)
                )
            )

    with Performer.batch_write() as batch:
        for performer_name, programs in programs_by_performer.items():
            performer: Performer
            for performer in Performer.name_gsi.query(performer_name, limit=1):
                if not performer.programs:
                    performer.programs = sorted(list(programs))
                    batch.save(performer)
                elif set(performer.programs) != programs:
                    performer.programs = sorted(list(programs | set(performer.programs)))
                    batch.save(performer)


def lambda_handler(event, context):
    record = event["Records"][0]
    body = json.loads(record["body"])
    main(body["studio_name"], body["studio_code"])
    return {
        "statusCode": 200,
        "body": "success",
    }
