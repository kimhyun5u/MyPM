"""메모리 기반 Tasks 리포지토리 구현."""

from __future__ import annotations

import uuid
from collections import defaultdict
from datetime import date

from mypm.domain.tasks.entities import Retrospective, Task, TaskStatus
from mypm.domain.tasks.repositories import RetrospectiveRepository, TaskRepository


class InMemoryTaskRepository(TaskRepository):
    """메모리 기반 Task 저장소."""

    def __init__(self) -> None:
        self._tasks: dict[uuid.UUID, Task] = {}
        self._by_status: dict[TaskStatus, set[uuid.UUID]] = defaultdict(set)

    async def add(self, task: Task) -> Task:
        self._tasks[task.id] = task
        self._by_status[task.status].add(task.id)
        return task

    async def get(self, task_id: uuid.UUID) -> Task | None:
        return self._tasks.get(task_id)

    async def list_by_status(self, status: str | None = None) -> list[Task]:
        if status is None:
            return list(self._tasks.values())

        try:
            status_enum = TaskStatus(status)
        except ValueError:
            return []

        return [self._tasks[task_id] for task_id in self._by_status.get(status_enum, set())]

    async def update(self, task: Task) -> Task:
        if task.id not in self._tasks:
            raise ValueError("Task not found")

        # 상태가 바뀌었다면 인덱스 업데이트
        for status, task_ids in self._by_status.items():
            if task.id in task_ids and status != task.status:
                task_ids.remove(task.id)
        self._by_status[task.status].add(task.id)

        self._tasks[task.id] = task
        return task

    async def delete(self, task_id: uuid.UUID) -> None:
        task = self._tasks.pop(task_id, None)
        if task is None:
            return

        self._by_status[task.status].discard(task_id)


class InMemoryRetrospectiveRepository(RetrospectiveRepository):
    """메모리 기반 Retrospective 저장소."""

    def __init__(self) -> None:
        self._retrospectives: dict[uuid.UUID, Retrospective] = {}
        self._by_date: dict[date, uuid.UUID] = {}

    async def add(self, retrospective: Retrospective) -> Retrospective:
        self._retrospectives[retrospective.id] = retrospective
        self._by_date[retrospective.date] = retrospective.id
        return retrospective

    async def get_by_date(self, retrospective_date: date) -> Retrospective | None:
        retrospective_id = self._by_date.get(retrospective_date)
        if retrospective_id is None:
            return None

        return self._retrospectives.get(retrospective_id)

    async def get(self, retrospective_id: uuid.UUID) -> Retrospective | None:
        return self._retrospectives.get(retrospective_id)

    async def update(self, retrospective: Retrospective) -> Retrospective:
        if retrospective.id not in self._retrospectives:
            raise ValueError("Retrospective not found")

        self._retrospectives[retrospective.id] = retrospective
        self._by_date[retrospective.date] = retrospective.id
        return retrospective


