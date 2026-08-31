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


def _ensure_column(conn: sqlite3.Connection, table: str, column: str, decl: str) -> None:
    cols = [row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    if column not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {decl}")


def _migrate_review_schedule_pk(conn: sqlite3.Connection) -> None:
    """review_schedule used to be keyed by problem_id alone; it now needs a
    composite (nickname, problem_id) key so each learner gets their own
    spaced-repetition schedule. SQLite can't alter a primary key in place,
    so rebuild the table when the old shape is detected."""
    exists = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='review_schedule'"
    ).fetchone()
    if not exists:
        return
    cols = [row[1] for row in conn.execute("PRAGMA table_info(review_schedule)").fetchall()]
    if "nickname" in cols:
        return
    conn.execute("ALTER TABLE review_schedule RENAME TO review_schedule_old")
    conn.execute(
        """
        CREATE TABLE review_schedule (
            nickname TEXT NOT NULL,
            problem_id TEXT NOT NULL,
            box INTEGER NOT NULL DEFAULT 0,
            next_review_at TEXT NOT NULL,
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            PRIMARY KEY (nickname, problem_id)
        )
        """
    )
    conn.execute(
        "INSERT INTO review_schedule (nickname, problem_id, box, next_review_at, updated_at) "
        "SELECT '', problem_id, box, next_review_at, updated_at FROM review_schedule_old"
    )
    conn.execute("DROP TABLE review_schedule_old")


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                nickname TEXT PRIMARY KEY,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT NOT NULL DEFAULT '',
                problem_id TEXT NOT NULL,
                code TEXT NOT NULL,
                passed INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        _ensure_column(conn, "attempts", "nickname", "TEXT NOT NULL DEFAULT ''")

        _migrate_review_schedule_pk(conn)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS review_schedule (
                nickname TEXT NOT NULL,
                problem_id TEXT NOT NULL,
                box INTEGER NOT NULL DEFAULT 0,
                next_review_at TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT (datetime('now')),
                PRIMARY KEY (nickname, problem_id)
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS review_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT NOT NULL DEFAULT '',
                problem_id TEXT NOT NULL,
                outcome TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        _ensure_column(conn, "review_events", "nickname", "TEXT NOT NULL DEFAULT ''")

        conn.commit()


# --- User profiles (nickname-only, no password — see project decision) ---


def create_user(nickname: str) -> bool:
    """Returns True if created, False if the nickname was already taken."""
    with get_connection() as conn:
        try:
            conn.execute(
                "INSERT INTO users (nickname) VALUES (?)",
                (nickname,),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False


def user_exists(nickname: str) -> bool:
    with get_connection() as conn:
        row = conn.execute("SELECT 1 FROM users WHERE nickname = ?", (nickname,)).fetchone()
    return row is not None


def save_attempt(nickname: str, problem_id: str, code: str, passed: bool) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO attempts (nickname, problem_id, code, passed) VALUES (?, ?, ?, ?)",
            (nickname, problem_id, code, int(passed)),
        )
        conn.commit()


def get_review_items(nickname: str) -> list[dict]:
    """One entry per problem that has ever been failed, with attempt/fail
    counts and whether the most recent attempt for it passed."""
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT problem_id, code, passed, created_at FROM attempts "
            "WHERE nickname = ? ORDER BY created_at ASC, id ASC",
            (nickname,),
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


def get_solved_problem_ids(nickname: str) -> set[str]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT problem_id FROM attempts WHERE nickname = ? AND passed = 1",
            (nickname,),
        ).fetchall()
    return {row[0] for row in rows}


def get_fail_counts_by_problem(nickname: str) -> dict[str, int]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT problem_id, COUNT(*) FROM attempts "
            "WHERE nickname = ? AND passed = 0 GROUP BY problem_id",
            (nickname,),
        ).fetchall()
    return {row[0]: row[1] for row in rows}


def get_attempt_stats(nickname: str) -> tuple[int, int]:
    """Returns (total_attempts, passed_attempts)."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT COUNT(*), SUM(passed) FROM attempts WHERE nickname = ?", (nickname,)
        ).fetchone()
    return row[0] or 0, row[1] or 0


def get_active_dates(nickname: str) -> list[str]:
    """Distinct calendar dates (YYYY-MM-DD) with at least one attempt, ascending."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT date(created_at) AS d FROM attempts "
            "WHERE nickname = ? ORDER BY d ASC",
            (nickname,),
        ).fetchall()
    return [row[0] for row in rows]


def record_review_outcome(nickname: str, problem_id: str, passed: bool) -> None:
    """Leitner-style spaced repetition bookkeeping, run after every grading.

    A wrong answer (re)enters the problem into review at box 0, due
    tomorrow. A right answer only matters here if the problem was already
    in the rotation (i.e. it had been wrong before) — advance it to the
    next box, or graduate it out of the rotation entirely once it clears
    the last box.
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT box FROM review_schedule WHERE nickname = ? AND problem_id = ?",
            (nickname, problem_id),
        ).fetchone()

        if not passed:
            next_review = (date.today() + timedelta(days=BOX_INTERVALS_DAYS[0])).isoformat()
            conn.execute(
                """
                INSERT INTO review_schedule (nickname, problem_id, box, next_review_at, updated_at)
                VALUES (?, ?, 0, ?, datetime('now'))
                ON CONFLICT(nickname, problem_id) DO UPDATE SET
                    box = 0, next_review_at = excluded.next_review_at, updated_at = datetime('now')
                """,
                (nickname, problem_id, next_review),
            )
            conn.execute(
                "INSERT INTO review_events (nickname, problem_id, outcome) VALUES (?, ?, 'missed')",
                (nickname, problem_id),
            )
            conn.commit()
            return

        if row is None:
            return  # passed, and was never in the review rotation — nothing to do.

        next_box = row[0] + 1
        if next_box >= len(BOX_INTERVALS_DAYS):
            conn.execute(
                "DELETE FROM review_schedule WHERE nickname = ? AND problem_id = ?",
                (nickname, problem_id),
            )
            outcome = "graduated"
        else:
            next_review = (date.today() + timedelta(days=BOX_INTERVALS_DAYS[next_box])).isoformat()
            conn.execute(
                "UPDATE review_schedule SET box = ?, next_review_at = ?, updated_at = datetime('now') "
                "WHERE nickname = ? AND problem_id = ?",
                (next_box, next_review, nickname, problem_id),
            )
            outcome = "advanced"
        conn.execute(
            "INSERT INTO review_events (nickname, problem_id, outcome) VALUES (?, ?, ?)",
            (nickname, problem_id, outcome),
        )
        conn.commit()


def get_due_review_problem_ids(nickname: str) -> list[str]:
    today = date.today().isoformat()
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT problem_id FROM review_schedule "
            "WHERE nickname = ? AND next_review_at <= ? ORDER BY next_review_at ASC",
            (nickname, today),
        ).fetchall()
    return [row[0] for row in rows]


# --- Report queries (date-range scoped, both bounds inclusive, YYYY-MM-DD) ---


def get_attempt_stats_in_range(nickname: str, start: str, end: str) -> tuple[int, int]:
    """Returns (total_attempts, passed_attempts) within [start, end]."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT COUNT(*), SUM(passed) FROM attempts "
            "WHERE nickname = ? AND date(created_at) BETWEEN ? AND ?",
            (nickname, start, end),
        ).fetchone()
    return row[0] or 0, row[1] or 0


def get_active_dates_in_range(nickname: str, start: str, end: str) -> list[str]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT date(created_at) AS d FROM attempts "
            "WHERE nickname = ? AND date(created_at) BETWEEN ? AND ? ORDER BY d ASC",
            (nickname, start, end),
        ).fetchall()
    return [row[0] for row in rows]


def get_fail_counts_in_range(nickname: str, start: str, end: str) -> dict[str, int]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT problem_id, COUNT(*) FROM attempts "
            "WHERE nickname = ? AND passed = 0 AND date(created_at) BETWEEN ? AND ? "
            "GROUP BY problem_id",
            (nickname, start, end),
        ).fetchall()
    return {row[0]: row[1] for row in rows}


def get_newly_solved_problem_ids(nickname: str, start: str, end: str) -> list[str]:
    """Problems whose *first-ever* passing attempt falls within [start, end] —
    i.e. genuinely learned during this period, not a re-solve of old work."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT problem_id, MIN(created_at) AS first_pass
            FROM attempts
            WHERE nickname = ? AND passed = 1
            GROUP BY problem_id
            HAVING date(first_pass) BETWEEN ? AND ?
            """,
            (nickname, start, end),
        ).fetchall()
    return [row[0] for row in rows]


def get_review_event_counts_in_range(nickname: str, start: str, end: str) -> dict[str, int]:
    """Counts of review_events by outcome ('missed' | 'advanced' | 'graduated')."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT outcome, COUNT(*) FROM review_events "
            "WHERE nickname = ? AND date(created_at) BETWEEN ? AND ? GROUP BY outcome",
            (nickname, start, end),
        ).fetchall()
    return {row[0]: row[1] for row in rows}
