"""Retrospective API 스키마."""

from __future__ import annotations

import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class RetrospectiveCreateSchema(BaseModel):
    title: str = Field(..., description="회고 제목")
    summary: str | None = Field(None, description="회고 요약")
    date: datetime.date | None = Field(None, description="회고 일자")


class RetrospectiveResponseSchema(BaseModel):
    id: UUID
    title: str
    summary: str | None
    date: datetime.date
    tasks: list[UUID]

    class Config:
        from_attributes = True


