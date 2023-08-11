from ...models import Performer
from ...scraping_functions import scraping_performer


def main():
    for item in scraping_performer():
        with Performer.batch_write() as batch:
            batch.save(Performer(**item.model_dump()))


def lambda_handler(event, context):
    main()
    return {
        "statusCode": 200,
        "body": "success",
    }
