from fastapi import APIRouter, Depends, HTTPException

from app import content_loader, db
from app.code_checks import check_required_constructs
from app.deps import require_nickname
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
def submit(req: SubmitRequest, nickname: str = Depends(require_nickname)):
    expected = content_loader.get_expected_stdout(req.problem_id)
    if expected is None:
        raise HTTPException(status_code=404, detail="문제를 찾을 수 없습니다.")

    # 채점은 항상 서버가 정해둔 고정 입력값을 쓴다 — 학습자가 입력한 값에 따라
    # 정답 비교가 흔들리지 않도록 하기 위함이다.
    stdin = content_loader.get_expected_stdin(req.problem_id)
    stdout, stderr, timed_out = run_python(req.code, stdin)
    output_matches = not timed_out and _outputs_match(stdout, expected)

    # 출력만 맞으면 통과시키면, 로직 없이 정답 문자열을 그대로 print()해도
    # 통과해버린다. 문제가 요구하는 구성 요소(반복문/함수 정의 등)를 실제로
    # 썼는지도 함께 확인한다 — "어떻게" 풀었는지는 안 보되, 아예 안 푼 건 아닌지는 본다.
    missing_constructs: list[str] = []
    if output_matches:
        required = content_loader.get_required_constructs(req.problem_id)
        if required:
            missing_constructs = check_required_constructs(req.code, required)

    passed = output_matches and not missing_constructs

    db.save_attempt(nickname, req.problem_id, req.code, passed)
    db.record_review_outcome(nickname, req.problem_id, passed)

    if passed:
        feedback = "정확합니다! 다음 문제로 넘어가도 좋아요."
    elif missing_constructs:
        feedback = (
            "출력은 맞지만 이 문제가 요구하는 방식으로 풀지 않았어요. "
            f"다음을 사용해서 다시 작성해보세요: {', '.join(missing_constructs)}"
        )
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
