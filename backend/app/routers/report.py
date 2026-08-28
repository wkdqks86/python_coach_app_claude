from datetime import date, timedelta

from fastapi import APIRouter

from app import content_loader, db
from app.routers.progress import _compute_streak
from app.schemas import LearningReport, WeakConcept

router = APIRouter(prefix="/api", tags=["report"])

REPORT_WINDOW_DAYS = 7
WEAK_CONCEPT_LIMIT = 5


def _highlight_message(problems_solved: int, active_days: int, reviews_advanced: int) -> str:
    if problems_solved == 0 and active_days == 0:
        return "이번 주는 아직 학습 기록이 없어요. 오늘 한 문제만 풀어볼까요?"
    if active_days >= 5:
        return f"이번 주 {active_days}일이나 학습하셨네요! 꾸준함이 최고의 무기입니다."
    if problems_solved == 0 and reviews_advanced > 0:
        return f"새 문제는 없었지만 복습으로 {reviews_advanced}개 문제를 더 단단히 다졌어요."
    if problems_solved > 0:
        return f"이번 주 {problems_solved}문제를 새로 해결했어요. 좋은 페이스예요!"
    return "이번 주도 조금씩 나아가고 있어요."


@router.get("/report", response_model=LearningReport)
def report():
    end = date.today()
    start = end - timedelta(days=REPORT_WINDOW_DAYS - 1)
    start_s, end_s = start.isoformat(), end.isoformat()

    active_dates_period = db.get_active_dates_in_range(start_s, end_s)
    total_attempts, passed_attempts = db.get_attempt_stats_in_range(start_s, end_s)
    newly_solved = db.get_newly_solved_problem_ids(start_s, end_s)
    review_counts = db.get_review_event_counts_in_range(start_s, end_s)
    fail_counts = db.get_fail_counts_in_range(start_s, end_s)

    new_concepts = {
        content_loader.get_problem_concept(pid)
        for pid in newly_solved
        if content_loader.get_problem_concept(pid) is not None
    }

    concept_fail_totals: dict[str, int] = {}
    for problem_id, count in fail_counts.items():
        concept_id = content_loader.get_problem_concept(problem_id)
        if concept_id is None:
            continue
        concept_fail_totals[concept_id] = concept_fail_totals.get(concept_id, 0) + count

    weak_concepts = sorted(
        (
            WeakConcept(
                concept_id=concept_id,
                concept_title=content_loader.get_concept_title(concept_id) or concept_id,
                fail_count=count,
            )
            for concept_id, count in concept_fail_totals.items()
        ),
        key=lambda w: w.fail_count,
        reverse=True,
    )[:WEAK_CONCEPT_LIMIT]

    reviews_advanced = review_counts.get("advanced", 0)
    reviews_graduated = review_counts.get("graduated", 0)
    reviews_missed = review_counts.get("missed", 0)

    return LearningReport(
        period_start=start_s,
        period_end=end_s,
        period_length_days=REPORT_WINDOW_DAYS,
        active_days=len(active_dates_period),
        problems_solved=len(newly_solved),
        new_concepts=len(new_concepts),
        total_attempts=total_attempts,
        success_rate=(passed_attempts / total_attempts) if total_attempts else 0.0,
        reviews_advanced=reviews_advanced,
        reviews_graduated=reviews_graduated,
        reviews_missed=reviews_missed,
        weak_concepts=weak_concepts,
        streak_days=_compute_streak(db.get_active_dates()),
        highlight_message=_highlight_message(len(newly_solved), len(active_dates_period), reviews_advanced),
    )
