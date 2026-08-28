import sqlite3
from contextlib import contextmanager
from datetime import date, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "pycoach.db"

# Leitner box schedule: how many days until the next review at each box
# level. Missing a review resets the problem back to box 0. Passing the
# last box (14 days later) graduates the problem out of the rotation.
BOX_INTERVALS_DAYS = [1, 3, 7, 14]


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_id TEXT NOT NULL,
                code TEXT NOT NULL,
                passed INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS review_schedule (
                problem_id TEXT PRIMARY KEY,
                box INTEGER NOT NULL DEFAULT 0,
                next_review_at TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS review_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_id TEXT NOT NULL,
                outcome TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        conn.commit()


def save_attempt(problem_id: str, code: str, passed: bool) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO attempts (problem_id, code, passed) VALUES (?, ?, ?)",
            (problem_id, code, int(passed)),
        )
        conn.commit()


def get_review_items() -> list[dict]:
    """One entry per problem that has ever been failed, with attempt/fail
    counts and whether the most recent attempt for it passed."""
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT problem_id, code, passed, created_at FROM attempts "
            "ORDER BY created_at ASC, id ASC"
        ).fetchall()

    by_problem: dict[str, dict] = {}
    for row in rows:
        entry = by_problem.setdefault(
            row["problem_id"], {"attempt_count": 0, "fail_count": 0}
        )
        entry["attempt_count"] += 1
        if not row["passed"]:
            entry["fail_count"] += 1
        entry["last_code"] = row["code"]
        entry["last_attempt_at"] = row["created_at"]
        entry["resolved"] = bool(row["passed"])

    return [
        {"problem_id": problem_id, **data}
        for problem_id, data in by_problem.items()
        if data["fail_count"] > 0
    ]


def get_solved_problem_ids() -> set[str]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT problem_id FROM attempts WHERE passed = 1"
        ).fetchall()
    return {row[0] for row in rows}


def get_fail_counts_by_problem() -> dict[str, int]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT problem_id, COUNT(*) FROM attempts WHERE passed = 0 GROUP BY problem_id"
        ).fetchall()
    return {row[0]: row[1] for row in rows}


def get_attempt_stats() -> tuple[int, int]:
    """Returns (total_attempts, passed_attempts)."""
    with get_connection() as conn:
        row = conn.execute("SELECT COUNT(*), SUM(passed) FROM attempts").fetchone()
    return row[0] or 0, row[1] or 0


def get_active_dates() -> list[str]:
    """Distinct calendar dates (YYYY-MM-DD) with at least one attempt, ascending."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT date(created_at) AS d FROM attempts ORDER BY d ASC"
        ).fetchall()
    return [row[0] for row in rows]


def record_review_outcome(problem_id: str, passed: bool) -> None:
    """Leitner-style spaced repetition bookkeeping, run after every grading.

    A wrong answer (re)enters the problem into review at box 0, due
    tomorrow. A right answer only matters here if the problem was already
    in the rotation (i.e. it had been wrong before) — advance it to the
    next box, or graduate it out of the rotation entirely once it clears
    the last box.
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT box FROM review_schedule WHERE problem_id = ?", (problem_id,)
        ).fetchone()

        if not passed:
            next_review = (date.today() + timedelta(days=BOX_INTERVALS_DAYS[0])).isoformat()
            conn.execute(
                """
                INSERT INTO review_schedule (problem_id, box, next_review_at, updated_at)
                VALUES (?, 0, ?, datetime('now'))
                ON CONFLICT(problem_id) DO UPDATE SET
                    box = 0, next_review_at = excluded.next_review_at, updated_at = datetime('now')
                """,
                (problem_id, next_review),
            )
            conn.execute(
                "INSERT INTO review_events (problem_id, outcome) VALUES (?, 'missed')",
                (problem_id,),
            )
            conn.commit()
            return

        if row is None:
            return  # passed, and was never in the review rotation — nothing to do.

        next_box = row[0] + 1
        if next_box >= len(BOX_INTERVALS_DAYS):
            conn.execute("DELETE FROM review_schedule WHERE problem_id = ?", (problem_id,))
            outcome = "graduated"
        else:
            next_review = (date.today() + timedelta(days=BOX_INTERVALS_DAYS[next_box])).isoformat()
            conn.execute(
                "UPDATE review_schedule SET box = ?, next_review_at = ?, updated_at = datetime('now') "
                "WHERE problem_id = ?",
                (next_box, next_review, problem_id),
            )
            outcome = "advanced"
        conn.execute(
            "INSERT INTO review_events (problem_id, outcome) VALUES (?, ?)",
            (problem_id, outcome),
        )
        conn.commit()


def get_due_review_problem_ids() -> list[str]:
    today = date.today().isoformat()
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT problem_id FROM review_schedule WHERE next_review_at <= ? ORDER BY next_review_at ASC",
            (today,),
        ).fetchall()
    return [row[0] for row in rows]


# --- Report queries (date-range scoped, both bounds inclusive, YYYY-MM-DD) ---


def get_attempt_stats_in_range(start: str, end: str) -> tuple[int, int]:
    """Returns (total_attempts, passed_attempts) within [start, end]."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT COUNT(*), SUM(passed) FROM attempts WHERE date(created_at) BETWEEN ? AND ?",
            (start, end),
        ).fetchone()
    return row[0] or 0, row[1] or 0


def get_active_dates_in_range(start: str, end: str) -> list[str]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT date(created_at) AS d FROM attempts WHERE date(created_at) BETWEEN ? AND ? ORDER BY d ASC",
            (start, end),
        ).fetchall()
    return [row[0] for row in rows]


def get_fail_counts_in_range(start: str, end: str) -> dict[str, int]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT problem_id, COUNT(*) FROM attempts "
            "WHERE passed = 0 AND date(created_at) BETWEEN ? AND ? GROUP BY problem_id",
            (start, end),
        ).fetchall()
    return {row[0]: row[1] for row in rows}


def get_newly_solved_problem_ids(start: str, end: str) -> list[str]:
    """Problems whose *first-ever* passing attempt falls within [start, end] —
    i.e. genuinely learned during this period, not a re-solve of old work."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT problem_id, MIN(created_at) AS first_pass
            FROM attempts
            WHERE passed = 1
            GROUP BY problem_id
            HAVING date(first_pass) BETWEEN ? AND ?
            """,
            (start, end),
        ).fetchall()
    return [row[0] for row in rows]


def get_review_event_counts_in_range(start: str, end: str) -> dict[str, int]:
    """Counts of review_events by outcome ('missed' | 'advanced' | 'graduated')."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT outcome, COUNT(*) FROM review_events "
            "WHERE date(created_at) BETWEEN ? AND ? GROUP BY outcome",
            (start, end),
        ).fetchall()
    return {row[0]: row[1] for row in rows}
