from typing import Sequence

from app.api.deps import get_entity_or_404
from app.db.session import get_session
from app.models.job_file_attachment import JobFileAttachment
from app.schemas.job_file_attachment import (
    JobFileAttachmentCreate,
    JobFileAttachmentRead,
    JobFileAttachmentUpdate,
)
from app.services.job_file_attachment import JobFileAttachmentService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/jobs/{job_id}/file-attachments",
    tags=["job-file-attachments"],
)

service = JobFileAttachmentService()
get_attachment_or_404 = get_entity_or_404(service.get)


@router.get("", response_model=list[JobFileAttachmentRead])
def list_job_file_attachments(
    job_id: int,
    offset: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
) -> Sequence[JobFileAttachment]:
    return service.find(session, job_id=job_id)[offset : offset + limit]


@router.get("/{attachment_id}", response_model=JobFileAttachmentRead)
def get_job_file_attachment(
    attachment: JobFileAttachment = Depends(get_attachment_or_404),
) -> JobFileAttachment:
    return attachment


@router.post(
    "", response_model=JobFileAttachmentRead, status_code=status.HTTP_201_CREATED
)
def create_job_file_attachment(
    job_id: int,
    data: JobFileAttachmentCreate,
    session: Session = Depends(get_session),
) -> JobFileAttachment:
    return service.create_attachment(session, job_id, data)


@router.patch("/{attachment_id}", response_model=JobFileAttachmentRead)
def update_job_file_attachment(
    data: JobFileAttachmentUpdate,
    attachment: JobFileAttachment = Depends(get_attachment_or_404),
    session: Session = Depends(get_session),
) -> JobFileAttachment:
    return service.update_attachment(session, attachment, data)


@router.delete("/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_file_attachment(
    attachment: JobFileAttachment = Depends(get_attachment_or_404),
    session: Session = Depends(get_session),
) -> None:
    service.delete(session, attachment)
    return None


@router.post("/{attachment_id}/detach", response_model=JobFileAttachmentRead)
def detach_job_file_attachment(
    attachment: JobFileAttachment = Depends(get_attachment_or_404),
    session: Session = Depends(get_session),
) -> JobFileAttachment:
    return service.detach_attachment(session, attachment)
