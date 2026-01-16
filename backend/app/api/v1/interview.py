from datetime import datetime
from typing import Sequence

from app.api.deps import get_entity_or_404
from app.db import get_session
from app.models.interview import Interview
from app.schemas.interview import InterviewCreate, InterviewRead, InterviewUpdate
from app.services.interview import InterviewService
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/jobs/{job_id}/interviews", tags=["interviews"])

service = InterviewService()
get_interview_or_404 = get_entity_or_404(service.get)


@router.get("", response_model=list[InterviewRead])
def list_interviews(
    job_id: int,
    offset: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
) -> Sequence[Interview]:
    return service.find(session, job_id=job_id)[offset : offset + limit]


@router.get("/{interview_id}", response_model=InterviewRead)
def get_interview(
    interview: Interview = Depends(get_interview_or_404),
) -> Interview:
    return interview


@router.post("", response_model=InterviewRead, status_code=status.HTTP_201_CREATED)
def create_interview(
    job_id: int,
    data: InterviewCreate,
    session: Session = Depends(get_session),
) -> Interview:
    return service.create_interview(session, job_id, data)


@router.patch("/{interview_id}", response_model=InterviewRead)
def update_interview(
    job_id: int,
    data: InterviewUpdate,
    interview: Interview = Depends(get_interview_or_404),
    session: Session = Depends(get_session),
) -> Interview:
    return service.update_interview(session, interview, data)


@router.delete("/{interview_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interview(
    interview: Interview = Depends(get_interview_or_404),
    session: Session = Depends(get_session),
) -> None:
    service.delete(session, interview)
    return None


@router.post("/{interview_id}/reschedule", response_model=InterviewRead)
def reschedule_interview(
    new_time: datetime = Query(..., alias="scheduled_at"),
    interview: Interview = Depends(get_interview_or_404),
    session: Session = Depends(get_session),
) -> Interview:
    return service.reschedule(session, interview, new_time)
