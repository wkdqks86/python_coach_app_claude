from fastapi import APIRouter

from app import content_loader, db
from app.schemas import ReviewItem

router = APIRouter(prefix="/api", tags=["review"])


@router.get("/review", response_model=list[ReviewItem])
def review():
    items = []
    for raw in db.get_review_items():
        level_id = content_loader.get_problem_level(raw["problem_id"])
        if level_id is None:
            continue
        items.append(
            ReviewItem(
                problem_id=raw["problem_id"],
                level_id=level_id,
                attempt_count=raw["attempt_count"],
                fail_count=raw["fail_count"],
                resolved=raw["resolved"],
                last_code=raw["last_code"],
                last_attempt_at=raw["last_attempt_at"],
            )
        )

    # 아직 못 푼 문제를 먼저, 그중에서는 최근에 시도한 것부터 보여준다.
    items.sort(key=lambda i: i.last_attempt_at, reverse=True)
    items.sort(key=lambda i: i.resolved)
    return items
