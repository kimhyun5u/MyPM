"""API 의존성 모듈."""

from collections.abc import AsyncIterator

from mypm.application.tasks import RetrospectiveService, TaskService
from mypm.infrastructure.tasks import InMemoryRetrospectiveRepository, InMemoryTaskRepository

_task_repository = InMemoryTaskRepository()
_retrospective_repository = InMemoryRetrospectiveRepository()
_task_service = TaskService(
    repository=_task_repository,
    retrospective_repository=_retrospective_repository,
)
_retrospective_service = RetrospectiveService(
    repository=_retrospective_repository,
    task_repository=_task_repository,
)


async def get_task_service() -> AsyncIterator[TaskService]:
    yield _task_service


async def get_retrospective_service() -> AsyncIterator[RetrospectiveService]:
    yield _retrospective_service


