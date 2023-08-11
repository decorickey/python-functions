from fastapi import APIRouter, HTTPException
from pynamodb.exceptions import DoesNotExist

from .models import Performer
from .schemas import PerformerSchema, ScheduleSchema

from .scraping_functions import scraping_schedule_by_performer

router = APIRouter()


@router.get("/performers/")
def get_performers() -> list[PerformerSchema]:
    return sorted(
        [PerformerSchema.model_validate(item) for item in Performer.scan()],
        key=lambda performer: performer.id,
    )


@router.get("/performers/{performer_id}/schedules/")
def get_schedules(performer_id: int) -> list[ScheduleSchema]:
    try:
        performer = Performer.get(performer_id)
    except DoesNotExist as ex:
        raise HTTPException(status_code=404) from ex
    return list(scraping_schedule_by_performer(performer.id, performer.name))


# @router.get("/reviews/")
# def get_reviews(username: str = Depends(get_current_username)) -> list[BmonsterReviewSchema]:
#     return [BmonsterReviewSchema.model_validate(item) for item in BmonsterReview.query(username)]


# @router.post("/reviews/")
# def post_reviews(
#     review: BmonsterReviewSchema, username: str = Depends(get_current_username)
# ) -> BmonsterReviewSchema:
#     return BmonsterReviewSchema.model_validate(review.save(username))
