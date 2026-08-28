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
