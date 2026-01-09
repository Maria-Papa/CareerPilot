from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models import Job, JobStatusHistory, JobFileAttachment
from app.enums import JobStatus
from app.repositories import JobRepository
from app.schemas import JobCreate, JobUpdate
from app.services import BaseService


class JobService(BaseService[Job]):
    repository: JobRepository

    def __init__(self):
        super().__init__(JobRepository())

    def create_job(self, session: Session, data: JobCreate) -> Job:
        job = Job(**data.model_dump())
        job.created_at = datetime.now(timezone.utc)
        return self.create(session, job)

    def update_job(self, session: Session, job: Job, data: JobUpdate) -> Job:
        values = data.model_dump(exclude_unset=True)
        return self.update(session, job, values)

    def change_status(self, session: Session, job: Job, new_status: JobStatus) -> Job:
        history = JobStatusHistory(job_id=job.id, status=new_status)
        session.add(history)

        job.current_status = new_status
        session.commit()
        session.refresh(job)
        return job

    def attach_file(
        self, session: Session, job: Job, file_id: int, version: int
    ) -> JobFileAttachment:
        attachment = JobFileAttachment(
            job_id=job.id,
            file_id=file_id,
            version=version,
            is_active=True,
            attached_at=datetime.now(timezone.utc),
        )
        session.add(attachment)
        session.commit()
        session.refresh(attachment)
        return attachment
