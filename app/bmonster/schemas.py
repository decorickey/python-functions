from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PerformerSchema(CustomBaseModel):
    id: int
    name: str
    programs: list[str] | None = None


class ScheduleSchema(CustomBaseModel):
    studio: str
    start_at: datetime = Field(alias="startAt")
    performer_name: str = Field(alias="performerName")
    program: str
    url: str = ""
