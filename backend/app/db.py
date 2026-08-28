import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "pycoach.db"


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
