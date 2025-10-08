"""Retrospective 관련 API 라우터."""

from __future__ import annotations

import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status

from mypm.application.tasks import RetrospectiveService
from mypm.application.tasks.dto import RetrospectiveCreateInput, RetrospectiveOutput
from mypm.presentation.api.dependencies import get_retrospective_service
from mypm.presentation.api.schemas.retrospective import (
    RetrospectiveCreateSchema,
    RetrospectiveResponseSchema,
)

router = APIRouter()


@router.post("/", response_model=RetrospectiveResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_retrospective(
    payload: RetrospectiveCreateSchema,
    service: RetrospectiveService = Depends(get_retrospective_service),
) -> RetrospectiveResponseSchema:
    retro_input = RetrospectiveCreateInput(**payload.model_dump())
    created = await service.create_retrospective(retro_input)
    return RetrospectiveResponseSchema.model_validate(created)


@router.post("/{retrospective_id}/tasks/{task_id}", response_model=RetrospectiveResponseSchema)
async def attach_task(
    retrospective_id: uuid.UUID,
    task_id: uuid.UUID,
    service: RetrospectiveService = Depends(get_retrospective_service),
) -> RetrospectiveResponseSchema:
    try:
        attached = await service.attach_task(retrospective_id, task_id)
        return RetrospectiveResponseSchema.model_validate(attached)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/date/{retro_date}", response_model=RetrospectiveResponseSchema | None)
async def get_retrospective_by_date(
    retro_date: date,
    service: RetrospectiveService = Depends(get_retrospective_service),
) -> RetrospectiveResponseSchema | None:
    result = await service.get_summary(retro_date)
    if result is None:
        return None

    return RetrospectiveResponseSchema.model_validate(result)


