from fastapi import APIRouter, HTTPException

from app import content_loader
from app.schemas import Level, LevelSummary

router = APIRouter(prefix="/api/levels", tags=["levels"])


@router.get("", response_model=list[LevelSummary])
def list_levels():
    return content_loader.list_levels()


@router.get("/{level_id}", response_model=Level)
def get_level(level_id: int):
    level = content_loader.get_level(level_id)
    if level is None:
        raise HTTPException(status_code=404, detail="레벨을 찾을 수 없습니다.")
    return level
