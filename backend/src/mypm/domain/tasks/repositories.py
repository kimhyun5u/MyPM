"""Tasks 도메인 리포지토리 인터페이스."""

from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from datetime import date

from mypm.domain.tasks.entities import Retrospective, Task


class TaskRepository(ABC):
    """Task 리포지토리 인터페이스."""

    @abstractmethod
    async def add(self, task: Task) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def get(self, task_id: uuid.UUID) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: str | None = None) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, task: Task) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, task_id: uuid.UUID) -> None:
        raise NotImplementedError


class RetrospectiveRepository(ABC):
    """Retrospective 리포지토리 인터페이스."""

    @abstractmethod
    async def add(self, retrospective: Retrospective) -> Retrospective:
        raise NotImplementedError

    @abstractmethod
    async def get_by_date(self, retrospective_date: date) -> Retrospective | None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, retrospective_id: uuid.UUID) -> Retrospective | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, retrospective: Retrospective) -> Retrospective:
        raise NotImplementedError


