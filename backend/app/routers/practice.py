from fastapi import APIRouter, HTTPException

from app import content_loader, db
from app.execution import run_python
from app.schemas import RunRequest, RunResult, SubmitRequest, SubmitResult

router = APIRouter(prefix="/api", tags=["practice"])


@router.post("/run", response_model=RunResult)
def run(req: RunRequest):
    stdout, stderr, timed_out = run_python(req.code)
    return RunResult(stdout=stdout, stderr=stderr, timed_out=timed_out)


@router.post("/submit", response_model=SubmitResult)
def submit(req: SubmitRequest):
    expected = content_loader.get_expected_stdout(req.problem_id)
    if expected is None:
        raise HTTPException(status_code=404, detail="문제를 찾을 수 없습니다.")

    stdout, stderr, timed_out = run_python(req.code)
    passed = not timed_out and stdout.rstrip("\n") == expected.rstrip("\n")

    db.save_attempt(req.problem_id, req.code, passed)

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
