from typing import Sequence

from app.api.deps import get_session
from app.core.errors import EntityNotFoundError
from app.models.job_tag import JobTag
from app.schemas.job_tag import JobTagCreate, JobTagRead, JobTagUpdate
from app.services.job_tag import JobTagService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/jobs/{job_id}/tags",
    tags=["job-tags"],
)

service = JobTagService()


def get_tag_link_or_404(
    job_id: int,
    tag_id: int,
    session: Session = Depends(get_session),
) -> JobTag:
    link = service.get_link(session, job_id, tag_id)
    if link is None:
        raise EntityNotFoundError("JobTag not found")
    return link


@router.get("", response_model=list[JobTagRead])
def list_job_tags(
    job_id: int,
    session: Session = Depends(get_session),
) -> Sequence[JobTag]:
    return service.find(session, job_id=job_id)


@router.post("", response_model=JobTagRead, status_code=status.HTTP_201_CREATED)
def create_job_tag(
    job_id: int,
    data: JobTagCreate,
    session: Session = Depends(get_session),
) -> JobTag:
    return service.create_tag(session, job_id, data)


@router.patch("/{tag_id}", response_model=JobTagRead)
def update_job_tag(
    job_id: int,
    tag_id: int,
    data: JobTagUpdate,
    link: JobTag = Depends(get_tag_link_or_404),
    session: Session = Depends(get_session),
) -> JobTag:
    return service.update_tag(session, link, data)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_tag(
    job_id: int,
    tag_id: int,
    link: JobTag = Depends(get_tag_link_or_404),
    session: Session = Depends(get_session),
) -> None:
    service.delete(session, link)
    return None
