"""Tasks 도메인 엔티티."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date
import uuid
from enum import StrEnum


class TaskStatus(StrEnum):
    """Task 상태 정의."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"


@dataclass(slots=True, kw_only=True)
class Task:
    """Task 엔티티."""

    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    due_date: date | None = None
    retrospective_id: uuid.UUID | None = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def mark_in_progress(self) -> None:
        self.status = TaskStatus.IN_PROGRESS
        self.touch()

    def mark_done(self) -> None:
        self.status = TaskStatus.DONE
        self.touch()

    def mark_blocked(self) -> None:
        self.status = TaskStatus.BLOCKED
        self.touch()

    def attach_to_retrospective(self, retrospective_id: uuid.UUID) -> None:
        self.retrospective_id = retrospective_id
        self.touch()

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()


@dataclass(slots=True, kw_only=True)
class Retrospective:
    """매일 회고 엔티티."""

    title: str
    summary: str | None = None
    date: date = field(default_factory=date.today)
    tasks: list[uuid.UUID] = field(default_factory=list)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def add_task(self, task_id: uuid.UUID) -> None:
        if task_id not in self.tasks:
            self.tasks.append(task_id)
            self.touch()

    def remove_task(self, task_id: uuid.UUID) -> None:
        if task_id in self.tasks:
            self.tasks.remove(task_id)
            self.touch()

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()


