from typing import Sequence

from app.api.deps import get_entity_or_404
from app.db.session import get_session
from app.models.job_event import JobEvent
from app.schemas.job_event import JobEventCreate, JobEventRead, JobEventUpdate
from app.services.job_event import JobEventService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/jobs/{job_id}/job-events", tags=["job-events"])

service = JobEventService()
get_job_event_or_404 = get_entity_or_404(service.get_job_event)


@router.get("", response_model=list[JobEventRead])
def list_job_events(
    job_id: int,
    offset: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
) -> Sequence[JobEvent]:
    return service.list_for_job(session, job_id, offset=offset, limit=limit)


@router.get("/{job_event_id}", response_model=JobEventRead)
def get_job_event(
    event: JobEvent = Depends(get_job_event_or_404),
) -> JobEvent:
    return event


@router.post("", response_model=JobEventRead, status_code=status.HTTP_201_CREATED)
def create_job_event(
    job_id: int,
    data: JobEventCreate,
    session: Session = Depends(get_session),
) -> JobEvent:
    return service.create_for_job(session, job_id, data)


@router.patch("/{job_event_id}", response_model=JobEventRead)
def update_job_event(
    job_id: int,
    data: JobEventUpdate,
    event: JobEvent = Depends(get_job_event_or_404),
    session: Session = Depends(get_session),
) -> JobEvent:
    return service.update_for_job(session, event, job_id, data)


@router.delete("/{job_event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_event(
    event: JobEvent = Depends(get_job_event_or_404),
    session: Session = Depends(get_session),
) -> None:
    service.delete(session, event)
    return None
