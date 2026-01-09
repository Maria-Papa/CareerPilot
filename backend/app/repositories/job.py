from datetime import datetime
from sqlalchemy.orm import Session

from app.enums import JobStatus
from app.models import Job, JobStatusHistory, JobFileAttachment
from app.repositories import BaseRepository


class JobRepository(BaseRepository[Job]):
    def __init__(self):
        super().__init__(Job)

    def change_status(self, db: Session, job: Job, new_status: JobStatus) -> Job:
        try:
            history = JobStatusHistory(
                job_id=job.id,
                status=new_status,
            )
            db.add(history)

            job.current_status = new_status

            db.commit()
            db.refresh(job)
            return job
        except Exception:
            db.rollback()
            raise

    def attach_file(
        self,
        db: Session,
        job: Job,
        file_id: int,
        version: int,
    ) -> JobFileAttachment:
        try:
            attachment = JobFileAttachment(
                job_id=job.id,
                file_id=file_id,
                version=version,
                is_active=True,
                attached_at=datetime.utcnow(),
            )
            db.add(attachment)
            db.commit()
            db.refresh(attachment)
            return attachment
        except Exception:
            db.rollback()
            raise
