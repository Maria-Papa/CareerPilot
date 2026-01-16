from app.api.deps import get_current_user, get_session
from app.db.session import get_session
from app.enums.job_status import JobStatus
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreate, JobRead, JobUpdate
from app.services.job import JobService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/jobs", tags=["jobs"])

service = JobService()


@router.get("", response_model=list[JobRead])
def list_jobs(
    offset: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return service.list_for_user(session, current_user.id, offset=offset, limit=limit)


@router.get("/{job_id}", response_model=JobRead)
def get_job(
    job_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return service.get_for_user(session, job_id, current_user.id)


@router.post("", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_job(
    data: JobCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return service.create_job(session, data, current_user.id)


@router.patch("/{job_id}", response_model=JobRead)
def update_job(
    job_id: int,
    data: JobUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    job = service.get_for_user(session, job_id, current_user.id)
    return service.update_job(session, job, data)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    job = service.get_for_user(session, job_id, current_user.id)
    service.delete(session, job)
    return None


@router.post("/{job_id}/restore", response_model=JobRead)
def restore_job(
    job_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    job = service.get_including_deleted_for_user(session, job_id, current_user.id)
    service.restore(session, job)
    return job


@router.post("/{job_id}/status/{new_status}", response_model=JobRead)
def change_status(
    job_id: int,
    new_status: JobStatus,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    job = service.get_for_user(session, job_id, current_user.id)
    return service.change_status(session, job, new_status)


@router.post("/{job_id}/attachments", status_code=status.HTTP_201_CREATED)
def attach_file(
    job_id: int,
    file_id: int = 0,
    version: int = 1,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    job = service.get_for_user(session, job_id, current_user.id)
    return service.attach_file(session, job, file_id, version)
