from fastapi import APIRouter, HTTPException

from app import content_loader, db
from app.execution import run_python
from app.schemas import RunRequest, RunResult, SubmitRequest, SubmitResult

router = APIRouter(prefix="/api", tags=["practice"])

FLOAT_TOLERANCE = 1e-6


def _outputs_match(actual: str, expected: str) -> bool:
    """Exact match, with a fallback: a line that's purely a number is compared
    within a small tolerance instead of as text. This lets numpy/pandas
    problems pass even if two mathematically-equivalent computations produce
    a bit-different float repr (e.g. summing in a different order)."""
    a_lines = actual.rstrip("\n").split("\n")
    e_lines = expected.rstrip("\n").split("\n")
    if len(a_lines) != len(e_lines):
        return False
    for a_line, e_line in zip(a_lines, e_lines):
        if a_line == e_line:
            continue
        try:
            if abs(float(a_line) - float(e_line)) < FLOAT_TOLERANCE:
                continue
        except ValueError:
            pass
        return False
    return True


@router.post("/run", response_model=RunResult)
def run(req: RunRequest):
    stdout, stderr, timed_out = run_python(req.code, req.stdin)
    return RunResult(stdout=stdout, stderr=stderr, timed_out=timed_out)


@router.post("/submit", response_model=SubmitResult)
def submit(req: SubmitRequest):
    expected = content_loader.get_expected_stdout(req.problem_id)
    if expected is None:
        raise HTTPException(status_code=404, detail="문제를 찾을 수 없습니다.")

    # 채점은 항상 서버가 정해둔 고정 입력값을 쓴다 — 학습자가 입력한 값에 따라
    # 정답 비교가 흔들리지 않도록 하기 위함이다.
    stdin = content_loader.get_expected_stdin(req.problem_id)
    stdout, stderr, timed_out = run_python(req.code, stdin)
    passed = not timed_out and _outputs_match(stdout, expected)

    db.save_attempt(req.problem_id, req.code, passed)
    db.record_review_outcome(req.problem_id, passed)

    if passed:
        feedback = "정확합니다! 다음 문제로 넘어가도 좋아요."
    elif stderr:
        feedback = "코드를 실행하는 중 오류가 발생했어요. 아래 오류 메시지를 확인해보세요."
    elif timed_out:
        feedback = stderr
    else:
        feedback = "아직 정답이 아니에요. 출력 결과를 기대한 내용과 비교해보세요."

    return SubmitResult(
        passed=passed,
        stdout=stdout,
        stderr=stderr,
        # 오답일 때는 정답을 그대로 보여주지 않는다 — 힌트를 통해 스스로 찾도록 유도한다.
        expected_stdout=expected if passed else "",
        feedback=feedback,
    )
