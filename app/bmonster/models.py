import os

from pynamodb import attributes, indexes, models


class Performer(models.Model):
    class Meta:
        table_name = os.environ["BMONSTER_PERFORMER_TABLE"]
        region = "ap-northeast-1"

    class NameGSI(indexes.GlobalSecondaryIndex):
        class Meta:
            index_name = os.environ["BMONSTER_PERFORMER_NAME_GSI"]
            projection = indexes.AllProjection()

        name = attributes.UnicodeAttribute(hash_key=True)

    id = attributes.NumberAttribute(hash_key=True)
    name = attributes.UnicodeAttribute()
    name_gsi = NameGSI()
    programs = attributes.ListAttribute(of=attributes.UnicodeAttribute, null=True)


class Schedule(models.Model):
    class Meta:
        table_name = os.environ["BMONSTER_SCHEDULE_TABLE"]
        region = "ap-northeast-1"

    class PerformerGSI(indexes.GlobalSecondaryIndex):
        class Meta:
            index_name = os.environ["BMONSTER_SCHEDULE_PERFORMER_GSI"]
            projection = indexes.AllProjection()

        performer_name = attributes.UnicodeAttribute(hash_key=True)
        start_at = attributes.UTCDateTimeAttribute(range_key=True)

    studio = attributes.UnicodeAttribute(hash_key=True)
    start_at = attributes.UTCDateTimeAttribute(range_key=True)
    performer_name = attributes.UnicodeAttribute()
    program = attributes.UnicodeAttribute()
    ttl = attributes.TTLAttribute()
    performer_gsi = PerformerGSI()


if os.environ["STAGE"] == "local":
    HOST = "http://dynamodb-local:8000"
    BILLING_MODE = "PAY_PER_REQUEST"
    Performer.Meta.host = HOST
    Performer.Meta.billing_mode = BILLING_MODE
    Schedule.Meta.billing_mode = BILLING_MODE
    Schedule.Meta.host = HOST

    if not Performer.exists():
        Performer.create_table()
    if not Schedule.exists():
        Schedule.create_table()
