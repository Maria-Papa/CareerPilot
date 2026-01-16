from datetime import datetime
from typing import cast

from app.core.errors import EntityNotFoundError
from app.models.interview import Interview
from app.repositories.interview import InterviewRepository
from app.repositories.job import JobRepository
from app.schemas.interview import InterviewCreate, InterviewUpdate
from app.services.base import BaseService
from sqlalchemy.orm import Session


class InterviewService(BaseService[Interview]):
    def __init__(
        self,
        repository: InterviewRepository | None = None,
        job_repo: JobRepository | None = None,
    ) -> None:
        repository = repository or InterviewRepository()
        super().__init__(repository)
        self._job_repo = job_repo or JobRepository()

    @property
    def interview_repo(self) -> InterviewRepository:
        return cast(InterviewRepository, self.repository)

    def _validate_job(self, session: Session, job_id: int) -> None:
        if self._job_repo.get(session, job_id) is None:
            raise EntityNotFoundError("Job not found")

    def create_interview(
        self, session: Session, job_id: int, data: InterviewCreate
    ) -> Interview:
        self._validate_job(session, job_id)
        interview = Interview(job_id=job_id, **data.model_dump())
        return self.create(session, interview)

    def update_interview(
        self,
        session: Session,
        interview: Interview,
        data: InterviewUpdate,
    ) -> Interview:
        values = data.model_dump(exclude_unset=True)
        if "job_id" in values and values["job_id"] is not None:
            self._validate_job(session, values["job_id"])
        return self.update(session, interview, values)

    def reschedule(
        self,
        session: Session,
        interview: Interview,
        new_time: datetime,
    ) -> Interview:
        interview.scheduled_at = new_time
        session.commit()
        session.refresh(interview)
        return interview
