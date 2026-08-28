from pydantic import BaseModel


class ConceptCard(BaseModel):
    id: str
    title: str
    explanation: str
    example_code: str
    example_output: str


class Problem(BaseModel):
    id: str
    concept_id: str
    prompt: str
    starter_code: str
    hints: list[str]
    input_hint: str | None = None


class Level(BaseModel):
    id: int
    title: str
    goal: str
    concepts: list[ConceptCard]
    problems: list[Problem]


class LevelSummary(BaseModel):
    id: int
    title: str
    goal: str
    concept_count: int
    problem_count: int


class RunRequest(BaseModel):
    code: str
    stdin: str = ""


class RunResult(BaseModel):
    stdout: str
    stderr: str
    timed_out: bool


class SubmitRequest(BaseModel):
    problem_id: str
    code: str


class SubmitResult(BaseModel):
    passed: bool
    stdout: str
    stderr: str
    expected_stdout: str
    feedback: str


class ReviewItem(BaseModel):
    problem_id: str
    level_id: int
    attempt_count: int
    fail_count: int
    resolved: bool
    last_code: str
    last_attempt_at: str


class LevelProgress(BaseModel):
    level_id: int
    title: str
    total_problems: int
    solved_problems: int
    completion_rate: float


class WeakConcept(BaseModel):
    concept_id: str
    concept_title: str
    fail_count: int


class ProgressSummary(BaseModel):
    levels: list[LevelProgress]
    total_problems: int
    total_solved: int
    overall_completion_rate: float
    total_attempts: int
    passed_attempts: int
    success_rate: float
    weak_concepts: list[WeakConcept]
    streak_days: int
    active_days: int


class CoachRequest(BaseModel):
    problem_id: str
    code: str
    question: str


class CoachResponse(BaseModel):
    reply: str
    source: str  # "ai" | "fallback"


class SolvedProblems(BaseModel):
    problem_ids: list[str]
