from typing import Sequence

from app.models.job import Job
from app.models.job_file_attachment import JobFileAttachment
from app.models.job_status_history import JobStatusHistory
from app.repositories.soft_delete_base import SoftDeleteBaseRepository
from sqlalchemy.orm import Session


class JobRepository(SoftDeleteBaseRepository[Job]):
    def __init__(self) -> None:
        super().__init__(Job)

    def get_for_user(self, session: Session, job_id: int, user_id: int) -> Job | None:
        stmt = self._base_query().where(Job.id == job_id).where(Job.user_id == user_id)
        return session.execute(stmt).scalar_one_or_none()

    def list_for_user(
        self, session: Session, user_id: int, *, offset: int = 0, limit: int = 100
    ) -> Sequence[Job]:
        stmt = (
            self._base_query().where(Job.user_id == user_id).offset(offset).limit(limit)
        )
        return session.execute(stmt).scalars().all()

    def add_status_history(
        self, session: Session, history: JobStatusHistory
    ) -> JobStatusHistory:
        session.add(history)
        session.commit()
        session.refresh(history)
        return history

    def add_file_attachment(
        self, session: Session, attachment: JobFileAttachment
    ) -> JobFileAttachment:
        session.add(attachment)
        session.commit()
        session.refresh(attachment)
        return attachment
