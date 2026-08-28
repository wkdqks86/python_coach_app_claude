from datetime import date, timedelta

from fastapi import APIRouter

from app import content_loader, db
from app.schemas import LevelProgress, ProgressSummary, SolvedProblems, WeakConcept

router = APIRouter(prefix="/api", tags=["progress"])

WEAK_CONCEPT_LIMIT = 5


def _compute_streak(active_dates: list[str]) -> int:
    """Consecutive days up to today (or yesterday, if today has no activity yet)."""
    if not active_dates:
        return 0

    dates = {date.fromisoformat(d) for d in active_dates}
    cursor = date.today()
    if cursor not in dates:
        cursor -= timedelta(days=1)
        if cursor not in dates:
            return 0

    streak = 0
    while cursor in dates:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


@router.get("/solved", response_model=SolvedProblems)
def solved():
    return SolvedProblems(problem_ids=sorted(db.get_solved_problem_ids()))


@router.get("/progress", response_model=ProgressSummary)
def progress():
    solved_ids = db.get_solved_problem_ids()
    fail_counts = db.get_fail_counts_by_problem()
    total_attempts, passed_attempts = db.get_attempt_stats()
    active_dates = db.get_active_dates()

    levels: list[LevelProgress] = []
    total_problems = 0
    total_solved = 0
    for level_id in content_loader.all_level_ids():
        level = content_loader.get_level(level_id)
        solved = sum(1 for p in level.problems if p.id in solved_ids)
        levels.append(
            LevelProgress(
                level_id=level.id,
                title=level.title,
                total_problems=len(level.problems),
                solved_problems=solved,
                completion_rate=(solved / len(level.problems)) if level.problems else 0.0,
            )
        )
        total_problems += len(level.problems)
        total_solved += solved

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

    return ProgressSummary(
        levels=levels,
        total_problems=total_problems,
        total_solved=total_solved,
        overall_completion_rate=(total_solved / total_problems) if total_problems else 0.0,
        total_attempts=total_attempts,
        passed_attempts=passed_attempts,
        success_rate=(passed_attempts / total_attempts) if total_attempts else 0.0,
        weak_concepts=weak_concepts,
        streak_days=_compute_streak(active_dates),
        active_days=len(active_dates),
    )
