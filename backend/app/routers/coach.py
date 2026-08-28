from fastapi import APIRouter, HTTPException

from app import ai_coach, content_loader
from app.schemas import CoachRequest, CoachResponse

router = APIRouter(prefix="/api", tags=["coach"])

NO_KEY_MESSAGE = (
    "AI 코치를 쓰려면 backend/.env 파일에 ANTHROPIC_API_KEY 또는 OPENAI_API_KEY를 설정해주세요. "
    "설정 전까지는 아래 3단계 힌트를 활용해보세요."
)
ERROR_MESSAGE = "AI 코치 호출 중 문제가 발생했어요. 잠시 후 다시 시도하거나 힌트를 활용해보세요."


@router.post("/coach", response_model=CoachResponse)
def coach(req: CoachRequest):
    prompt = content_loader.get_problem_prompt(req.problem_id)
    if prompt is None:
        raise HTTPException(status_code=404, detail="문제를 찾을 수 없습니다.")

    try:
        reply = ai_coach.ask_coach(prompt, req.code, req.question)
        return CoachResponse(reply=reply, source="ai")
    except ai_coach.CoachUnavailable:
        return CoachResponse(reply=NO_KEY_MESSAGE, source="fallback")
    except ai_coach.CoachRequestFailed:
        return CoachResponse(reply=ERROR_MESSAGE, source="fallback")
