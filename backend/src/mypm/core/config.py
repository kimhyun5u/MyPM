"""애플리케이션 설정 모듈."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os


def _str_to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default

    return value.lower() in {"1", "true", "on", "yes"}


@dataclass(frozen=True)
class Settings:
    """환경 변수 기반 설정."""

    app_name: str = os.getenv("MYPM_APP_NAME", "MyPM API")
    version: str = os.getenv("MYPM_APP_VERSION", "0.1.0")
    debug: bool = _str_to_bool(os.getenv("MYPM_DEBUG"))
    host: str = os.getenv("MYPM_HOST", "0.0.0.0")
    port: int = int(os.getenv("MYPM_PORT", "8000"))
    reload: bool = _str_to_bool(os.getenv("MYPM_RELOAD"))


@lru_cache
def get_settings() -> Settings:
    """싱글톤 형태로 설정을 반환합니다."""

    return Settings()


__all__ = ["Settings", "get_settings"]

