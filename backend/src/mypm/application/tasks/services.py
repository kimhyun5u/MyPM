"""Tasks 애플리케이션 서비스."""

from __future__ import annotations

import uuid
from datetime import date

from mypm.application.tasks.dto import (
    RetrospectiveCreateInput,
    RetrospectiveOutput,
    TaskCreateInput,
    TaskOutput,
    TaskUpdateInput,
    to_task_outputs,
)
from mypm.domain.tasks.entities import Retrospective, Task
from mypm.domain.tasks.repositories import RetrospectiveRepository, TaskRepository


class TaskService:
    """Task 관련 애플리케이션 서비스."""

    def __init__(self, repository: TaskRepository, retrospective_repository: RetrospectiveRepository):
        self._repository = repository
        self._retrospective_repository = retrospective_repository

    async def create_task(self, data: TaskCreateInput) -> TaskOutput:
        task = Task(title=data.title, description=data.description, due_date=data.due_date)

        created = await self._repository.add(task)
        return TaskOutput.from_entity(created)

    async def list_tasks(self, status: str | None = None) -> list[TaskOutput]:
        tasks = await self._repository.list_by_status(status)
        return to_task_outputs(tasks)

    async def update_task(self, task_id: uuid.UUID, data: TaskUpdateInput) -> TaskOutput:
        task = await self._repository.get(task_id)
        if task is None:
            raise ValueError("Task not found")

        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description
        if data.status is not None:
            task.status = data.status
        if data.due_date is not None:
            task.due_date = data.due_date

        task.touch()
        updated = await self._repository.update(task)
        return TaskOutput.from_entity(updated)

    async def delete_task(self, task_id: uuid.UUID) -> None:
        await self._repository.delete(task_id)


class RetrospectiveService:
    """Retrospective 관련 애플리케이션 서비스."""

    def __init__(self, repository: RetrospectiveRepository, task_repository: TaskRepository):
        self._repository = repository
        self._task_repository = task_repository

    async def create_retrospective(self, data: RetrospectiveCreateInput) -> RetrospectiveOutput:
        retrospective = Retrospective(
            title=data.title,
            summary=data.summary,
            date=data.date or date.today(),
        )

        created = await self._repository.add(retrospective)
        return RetrospectiveOutput.from_entity(created)

    async def attach_task(self, retrospective_id: uuid.UUID, task_id: uuid.UUID) -> RetrospectiveOutput:
        retrospective = await self._repository.get(retrospective_id)
        if retrospective is None:
            raise ValueError("Retrospective not found")

        task = await self._task_repository.get(task_id)
        if task is None:
            raise ValueError("Task not found")

        retrospective.add_task(task.id)
        task.attach_to_retrospective(retrospective.id)

        await self._task_repository.update(task)
        updated = await self._repository.update(retrospective)

        return RetrospectiveOutput.from_entity(updated)

    async def get_summary(self, retrospective_date: date) -> RetrospectiveOutput | None:
        retrospective = await self._repository.get_by_date(retrospective_date)
        if retrospective is None:
            return None

        return RetrospectiveOutput.from_entity(retrospective)


