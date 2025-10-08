"""FastAPI 애플리케이션 팩토리."""

from fastapi import FastAPI

from mypm.core.config import get_settings
from mypm.presentation import api_router
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    """FastAPI 애플리케이션을 생성해 반환합니다."""

    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        debug=settings.debug,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    return app


# Uvicorn에서 경로 문자열로 참조할 수 있도록 모듈 레벨에서 앱을 초기화합니다.
app = create_app()

