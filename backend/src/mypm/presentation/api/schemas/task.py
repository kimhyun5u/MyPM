"""Task API 스키마."""

from __future__ import annotations

import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from mypm.domain.tasks.entities import TaskStatus


class TaskCreateSchema(BaseModel):
    title: str = Field(..., description="할 일 제목")
    description: str | None = Field(None, description="할 일 설명")
    due_date: datetime.date | None = Field(None, description="마감일")


class TaskUpdateSchema(BaseModel):
    title: str | None = Field(None, description="할 일 제목")
    description: str | None = Field(None, description="할 일 설명")
    status: TaskStatus | None = Field(None, description="할 일 상태")
    due_date: datetime.date | None = Field(None, description="마감일")


class TaskResponseSchema(BaseModel):
    id: UUID
    title: str
    description: str | None
    status: TaskStatus
    due_date: datetime.date | None
    retrospective_id: UUID | None

    class Config:
        from_attributes = True


