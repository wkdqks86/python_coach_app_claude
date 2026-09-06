import os
from contextlib import contextmanager
from datetime import date, timedelta

import psycopg
from psycopg.rows import dict_row

# A free Postgres (Neon/Supabase) instance, not the container's local disk —
# Render wipes local files on every redeploy since the free plan has no
# persistent disk, which once silently deleted a learner's whole history.
DATABASE_URL = os.environ["DATABASE_URL"]

# Leitner box schedule: how many days until the next review at each box
# level. Missing a review resets the problem back to box 0. Passing the
# last box (14 days later) graduates the problem out of the rotation.
BOX_INTERVALS_DAYS = [1, 3, 7, 14]


@contextmanager
def get_connection():
    conn = psycopg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    nickname TEXT PRIMARY KEY,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS attempts (
                    id SERIAL PRIMARY KEY,
                    nickname TEXT NOT NULL DEFAULT '',
                    problem_id TEXT NOT NULL,
                    code TEXT NOT NULL,
                    passed INTEGER NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS review_schedule (
                    nickname TEXT NOT NULL,
                    problem_id TEXT NOT NULL,
                    box INTEGER NOT NULL DEFAULT 0,
                    next_review_at TEXT NOT NULL,
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                    PRIMARY KEY (nickname, problem_id)
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS review_events (
                    id SERIAL PRIMARY KEY,
                    nickname TEXT NOT NULL DEFAULT '',
                    problem_id TEXT NOT NULL,
                    outcome TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                )
                """
            )
        conn.commit()


# --- User profiles (nickname-only, no password — see project decision) ---


def create_user(nickname: str) -> bool:
    """Returns True if created, False if the nickname was already taken."""
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO users (nickname) VALUES (%s)", (nickname,))
            conn.commit()
            return True
        except psycopg.errors.UniqueViolation:
            conn.rollback()
            return False


def user_exists(nickname: str) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE nickname = %s", (nickname,))
            row = cur.fetchone()
    return row is not None


def save_attempt(nickname: str, problem_id: str, code: str, passed: bool) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO attempts (nickname, problem_id, code, passed) VALUES (%s, %s, %s, %s)",
                (nickname, problem_id, code, int(passed)),
            )
        conn.commit()


def get_review_items(nickname: str) -> list[dict]:
    """One entry per problem that has ever been failed, with attempt/fail
    counts and whether the most recent attempt for it passed."""
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT problem_id, code, passed, created_at FROM attempts "
                "WHERE nickname = %s ORDER BY created_at ASC, id ASC",
                (nickname,),
            )
            rows = cur.fetchall()

    by_problem: dict[str, dict] = {}
    for row in rows:
        entry = by_problem.setdefault(
            row["problem_id"], {"attempt_count": 0, "fail_count": 0}
        )
        entry["attempt_count"] += 1
        if not row["passed"]:
            entry["fail_count"] += 1
        entry["last_code"] = row["code"]
        entry["last_attempt_at"] = row["created_at"].isoformat()
        entry["resolved"] = bool(row["passed"])

    return [
        {"problem_id": problem_id, **data}
        for problem_id, data in by_problem.items()
        if data["fail_count"] > 0
    ]


def get_solved_problem_ids(nickname: str) -> set[str]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT DISTINCT problem_id FROM attempts WHERE nickname = %s AND passed = 1",
                (nickname,),
            )
            rows = cur.fetchall()
    return {row[0] for row in rows}


def get_fail_counts_by_problem(nickname: str) -> dict[str, int]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT problem_id, COUNT(*) FROM attempts "
                "WHERE nickname = %s AND passed = 0 GROUP BY problem_id",
                (nickname,),
            )
            rows = cur.fetchall()
    return {row[0]: row[1] for row in rows}


def get_attempt_stats(nickname: str) -> tuple[int, int]:
    """Returns (total_attempts, passed_attempts)."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*), SUM(passed) FROM attempts WHERE nickname = %s", (nickname,)
            )
            row = cur.fetchone()
    return row[0] or 0, row[1] or 0


def get_active_dates(nickname: str) -> list[str]:
    """Distinct calendar dates (YYYY-MM-DD) with at least one attempt, ascending."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT DISTINCT date(created_at) AS d FROM attempts "
                "WHERE nickname = %s ORDER BY d ASC",
                (nickname,),
            )
            rows = cur.fetchall()
    return [row[0].isoformat() for row in rows]


def record_review_outcome(nickname: str, problem_id: str, passed: bool) -> None:
    """Leitner-style spaced repetition bookkeeping, run after every grading.

    A wrong answer (re)enters the problem into review at box 0, due
    tomorrow. A right answer only matters here if the problem was already
    in the rotation (i.e. it had been wrong before) — advance it to the
    next box, or graduate it out of the rotation entirely once it clears
    the last box.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT box FROM review_schedule WHERE nickname = %s AND problem_id = %s",
                (nickname, problem_id),
            )
            row = cur.fetchone()

            if not passed:
                next_review = (date.today() + timedelta(days=BOX_INTERVALS_DAYS[0])).isoformat()
                cur.execute(
                    """
                    INSERT INTO review_schedule (nickname, problem_id, box, next_review_at, updated_at)
                    VALUES (%s, %s, 0, %s, now())
                    ON CONFLICT (nickname, problem_id) DO UPDATE SET
                        box = 0, next_review_at = excluded.next_review_at, updated_at = now()
                    """,
                    (nickname, problem_id, next_review),
                )
                cur.execute(
                    "INSERT INTO review_events (nickname, problem_id, outcome) VALUES (%s, %s, 'missed')",
                    (nickname, problem_id),
                )
                conn.commit()
                return

            if row is None:
                return  # passed, and was never in the review rotation — nothing to do.

            next_box = row[0] + 1
            if next_box >= len(BOX_INTERVALS_DAYS):
                cur.execute(
                    "DELETE FROM review_schedule WHERE nickname = %s AND problem_id = %s",
                    (nickname, problem_id),
                )
                outcome = "graduated"
            else:
                next_review = (date.today() + timedelta(days=BOX_INTERVALS_DAYS[next_box])).isoformat()
                cur.execute(
                    "UPDATE review_schedule SET box = %s, next_review_at = %s, updated_at = now() "
                    "WHERE nickname = %s AND problem_id = %s",
                    (next_box, next_review, nickname, problem_id),
                )
                outcome = "advanced"
            cur.execute(
                "INSERT INTO review_events (nickname, problem_id, outcome) VALUES (%s, %s, %s)",
                (nickname, problem_id, outcome),
            )
        conn.commit()


def get_due_review_problem_ids(nickname: str) -> list[str]:
    today = date.today().isoformat()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT problem_id FROM review_schedule "
                "WHERE nickname = %s AND next_review_at <= %s ORDER BY next_review_at ASC",
                (nickname, today),
            )
            rows = cur.fetchall()
    return [row[0] for row in rows]


# --- Report queries (date-range scoped, both bounds inclusive, YYYY-MM-DD) ---


def get_attempt_stats_in_range(nickname: str, start: str, end: str) -> tuple[int, int]:
    """Returns (total_attempts, passed_attempts) within [start, end]."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*), SUM(passed) FROM attempts "
                "WHERE nickname = %s AND date(created_at) BETWEEN %s AND %s",
                (nickname, start, end),
            )
            row = cur.fetchone()
    return row[0] or 0, row[1] or 0


def get_active_dates_in_range(nickname: str, start: str, end: str) -> list[str]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT DISTINCT date(created_at) AS d FROM attempts "
                "WHERE nickname = %s AND date(created_at) BETWEEN %s AND %s ORDER BY d ASC",
                (nickname, start, end),
            )
            rows = cur.fetchall()
    return [row[0].isoformat() for row in rows]


def get_fail_counts_in_range(nickname: str, start: str, end: str) -> dict[str, int]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT problem_id, COUNT(*) FROM attempts "
                "WHERE nickname = %s AND passed = 0 AND date(created_at) BETWEEN %s AND %s "
                "GROUP BY problem_id",
                (nickname, start, end),
            )
            rows = cur.fetchall()
    return {row[0]: row[1] for row in rows}


def get_newly_solved_problem_ids(nickname: str, start: str, end: str) -> list[str]:
    """Problems whose *first-ever* passing attempt falls within [start, end] —
    i.e. genuinely learned during this period, not a re-solve of old work."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT problem_id, MIN(created_at) AS first_pass
                FROM attempts
                WHERE nickname = %s AND passed = 1
                GROUP BY problem_id
                HAVING date(MIN(created_at)) BETWEEN %s AND %s
                """,
                (nickname, start, end),
            )
            rows = cur.fetchall()
    return [row[0] for row in rows]


def get_review_event_counts_in_range(nickname: str, start: str, end: str) -> dict[str, int]:
    """Counts of review_events by outcome ('missed' | 'advanced' | 'graduated')."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT outcome, COUNT(*) FROM review_events "
                "WHERE nickname = %s AND date(created_at) BETWEEN %s AND %s GROUP BY outcome",
                (nickname, start, end),
            )
            rows = cur.fetchall()
    return {row[0]: row[1] for row in rows}
