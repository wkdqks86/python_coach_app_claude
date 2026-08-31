from fastapi import HTTPException, Query


def require_nickname(nickname: str = Query(..., min_length=1, max_length=20)) -> str:
    """Every per-user endpoint takes the acting learner's nickname as a query
    param (not a header) so it round-trips through fetch() cleanly even when
    it's Korean text — headers are ASCII-only in the Fetch API."""
    nickname = nickname.strip()
    if not nickname:
        raise HTTPException(status_code=401, detail="닉네임이 필요합니다.")
    return nickname
