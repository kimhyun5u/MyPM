"""API 라우터 초기화."""

from fastapi import APIRouter

from mypm.presentation.api.routes import retrospective, tasks


api_router = APIRouter()
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(retrospective.router, prefix="/retrospectives", tags=["retrospectives"])


__all__ = ["api_router"]

