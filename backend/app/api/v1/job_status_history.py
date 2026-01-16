from typing import Sequence

from app.api.deps import get_entity_or_404
from app.db.session import get_session
from app.models.job_status_history import JobStatusHistory
from app.schemas.job_status_history import (
    JobStatusHistoryCreate,
    JobStatusHistoryRead,
    JobStatusHistoryUpdate,
)
from app.services.job_status_history import JobStatusHistoryService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/jobs/{job_id}/status-history",
    tags=["job-status-history"],
)

service = JobStatusHistoryService()
get_history_or_404 = get_entity_or_404(service.get)


@router.get("", response_model=list[JobStatusHistoryRead])
def list_job_status_history(
    job_id: int,
    offset: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
) -> Sequence[JobStatusHistory]:
    return service.find(session, job_id=job_id)[offset : offset + limit]


@router.get("/{history_id}", response_model=JobStatusHistoryRead)
def get_job_status_history(
    history: JobStatusHistory = Depends(get_history_or_404),
) -> JobStatusHistory:
    return history


@router.post(
    "",
    response_model=JobStatusHistoryRead,
    status_code=status.HTTP_201_CREATED,
)
def create_job_status_history(
    job_id: int,
    data: JobStatusHistoryCreate,
    session: Session = Depends(get_session),
) -> JobStatusHistory:
    return service.create_history(session, job_id, data)


@router.patch("/{history_id}", response_model=JobStatusHistoryRead)
def update_job_status_history(
    data: JobStatusHistoryUpdate,
    history: JobStatusHistory = Depends(get_history_or_404),
    session: Session = Depends(get_session),
) -> JobStatusHistory:
    return service.update_history(session, history, data)


@router.delete("/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_status_history(
    history: JobStatusHistory = Depends(get_history_or_404),
    session: Session = Depends(get_session),
) -> None:
    service.delete(session, history)
    return None
