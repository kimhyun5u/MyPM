"""Task 관련 API 라우터."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from mypm.application.tasks import TaskService
from mypm.application.tasks.dto import TaskCreateInput, TaskOutput, TaskUpdateInput
from mypm.presentation.api.dependencies import get_task_service
from mypm.presentation.api.schemas.task import TaskCreateSchema, TaskResponseSchema, TaskUpdateSchema

router = APIRouter()


@router.post("/", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_task(
    payload: TaskCreateSchema,
    service: TaskService = Depends(get_task_service),
) -> TaskResponseSchema:
    task_input = TaskCreateInput(**payload.model_dump())
    created = await service.create_task(task_input)
    return TaskResponseSchema.model_validate(created)


@router.get("/", response_model=list[TaskResponseSchema])
async def list_tasks(
    status_filter: str | None = None,
    service: TaskService = Depends(get_task_service),
) -> list[TaskResponseSchema]:
    result = await service.list_tasks(status=status_filter)
    return [TaskResponseSchema.model_validate(item) for item in result]


@router.patch("/{task_id}", response_model=TaskResponseSchema)
async def update_task(
    task_id: uuid.UUID,
    payload: TaskUpdateSchema,
    service: TaskService = Depends(get_task_service),
) -> TaskResponseSchema:
    try:
        update_input = TaskUpdateInput(**payload.model_dump(exclude_unset=True))
        updated = await service.update_task(task_id, update_input)
        return TaskResponseSchema.model_validate(updated)
    except ValueError as exc:  # Task not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: uuid.UUID,
    service: TaskService = Depends(get_task_service),
) -> None:
    await service.delete_task(task_id)


