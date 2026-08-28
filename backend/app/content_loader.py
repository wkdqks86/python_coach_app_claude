import json
from pathlib import Path

from app.schemas import ConceptCard, Level, LevelSummary, Problem

CONTENT_DIR = Path(__file__).parent / "content"


def _load_raw_levels() -> dict[int, dict]:
    levels = {}
    for path in sorted(CONTENT_DIR.glob("level_*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        levels[data["id"]] = data
    return levels


_RAW_LEVELS = _load_raw_levels()

# problem_id -> expected_stdout, kept server-side only so the frontend can't peek at answers.
_EXPECTED_STDOUT: dict[str, str] = {
    problem["id"]: problem["expected_stdout"]
    for level in _RAW_LEVELS.values()
    for problem in level["problems"]
}

_PROBLEM_LEVEL: dict[str, int] = {
    problem["id"]: level["id"]
    for level in _RAW_LEVELS.values()
    for problem in level["problems"]
}

_PROBLEM_CONCEPT: dict[str, str] = {
    problem["id"]: problem["concept_id"]
    for level in _RAW_LEVELS.values()
    for problem in level["problems"]
}

_CONCEPT_TITLES: dict[str, str] = {
    concept["id"]: concept["title"]
    for level in _RAW_LEVELS.values()
    for concept in level["concepts"]
}


def list_levels() -> list[LevelSummary]:
    return [
        LevelSummary(
            id=data["id"],
            title=data["title"],
            goal=data["goal"],
            concept_count=len(data["concepts"]),
            problem_count=len(data["problems"]),
        )
        for data in sorted(_RAW_LEVELS.values(), key=lambda d: d["id"])
    ]


def get_level(level_id: int) -> Level | None:
    data = _RAW_LEVELS.get(level_id)
    if data is None:
        return None
    return Level(
        id=data["id"],
        title=data["title"],
        goal=data["goal"],
        concepts=[ConceptCard(**c) for c in data["concepts"]],
        problems=[
            Problem(
                id=p["id"],
                concept_id=p["concept_id"],
                prompt=p["prompt"],
                starter_code=p["starter_code"],
                hints=p["hints"],
            )
            for p in data["problems"]
        ],
    )


def get_expected_stdout(problem_id: str) -> str | None:
    return _EXPECTED_STDOUT.get(problem_id)


def get_problem_level(problem_id: str) -> int | None:
    return _PROBLEM_LEVEL.get(problem_id)


def get_problem_concept(problem_id: str) -> str | None:
    return _PROBLEM_CONCEPT.get(problem_id)


def get_concept_title(concept_id: str) -> str | None:
    return _CONCEPT_TITLES.get(concept_id)


def all_level_ids() -> list[int]:
    return sorted(_RAW_LEVELS.keys())
