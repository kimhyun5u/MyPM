"""Tasks 애플리케이션 DTO."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable
import uuid

from mypm.domain.tasks.entities import Retrospective, Task, TaskStatus


@dataclass(slots=True)
class TaskCreateInput:
    title: str
    description: str | None = None
    due_date: date | None = None


@dataclass(slots=True)
class TaskUpdateInput:
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    due_date: date | None = None


@dataclass(slots=True)
class TaskOutput:
    id: uuid.UUID
    title: str
    description: str | None
    status: TaskStatus
    due_date: date | None
    retrospective_id: uuid.UUID | None

    @classmethod
    def from_entity(cls, task: Task) -> "TaskOutput":
        return cls(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            due_date=task.due_date,
            retrospective_id=task.retrospective_id,
        )


@dataclass(slots=True)
class RetrospectiveCreateInput:
    title: str
    summary: str | None = None
    date: date | None = None


@dataclass(slots=True)
class RetrospectiveOutput:
    id: uuid.UUID
    title: str
    summary: str | None
    date: date
    tasks: list[uuid.UUID]

    @classmethod
    def from_entity(cls, retrospective: Retrospective) -> "RetrospectiveOutput":
        return cls(
            id=retrospective.id,
            title=retrospective.title,
            summary=retrospective.summary,
            date=retrospective.date,
            tasks=list(retrospective.tasks),
        )


def to_task_outputs(tasks: Iterable[Task]) -> list[TaskOutput]:
    return [TaskOutput.from_entity(task) for task in tasks]


