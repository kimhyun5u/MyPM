"""mypm CLI 엔트리포인트."""

import uvicorn

from mypm.app import create_app
from mypm.core.config import get_settings


def main() -> None:
    """FastAPI 서버를 실행합니다."""

    settings = get_settings()
    uvicorn.run(
        "mypm.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        factory=False,
    )


if __name__ == "__main__":
    main()
