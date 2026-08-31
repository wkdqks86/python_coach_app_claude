from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app import db

router = APIRouter(prefix="/api/profile", tags=["profile"])


class NicknameRequest(BaseModel):
    nickname: str


def _clean(nickname: str) -> str:
    nickname = nickname.strip()
    if not nickname or len(nickname) > 20 or any(c.isspace() for c in nickname):
        raise HTTPException(
            status_code=422, detail="닉네임은 공백 없이 1~20자로 입력해주세요."
        )
    return nickname


@router.post("/new")
def create_profile(req: NicknameRequest):
    nickname = _clean(req.nickname)
    if not db.create_user(nickname):
        raise HTTPException(
            status_code=409, detail="이미 사용 중인 닉네임이에요. 다른 닉네임을 입력해주세요."
        )
    return {"nickname": nickname}


@router.post("/resume")
def resume_profile(req: NicknameRequest):
    nickname = _clean(req.nickname)
    if not db.user_exists(nickname):
        raise HTTPException(
            status_code=404,
            detail="등록되지 않은 닉네임이에요. '처음 시작하기'를 이용해주세요.",
        )
    return {"nickname": nickname}
