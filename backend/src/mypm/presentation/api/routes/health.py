"""헬스 체크 엔드포인트."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Health Check")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


