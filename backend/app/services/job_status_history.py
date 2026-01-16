from typing import cast

from app.core.errors import EntityNotFoundError
from app.models.job_status_history import JobStatusHistory
from app.repositories import JobRepository, JobStatusHistoryRepository
from app.schemas import JobStatusHistoryCreate, JobStatusHistoryUpdate
from app.services.base import BaseService
from sqlalchemy.orm import Session


class JobStatusHistoryService(BaseService[JobStatusHistory]):
    def __init__(
        self,
        repository: JobStatusHistoryRepository | None = None,
        job_repo: JobRepository | None = None,
    ) -> None:
        repository = repository or JobStatusHistoryRepository()
        super().__init__(repository)
        self._job_repo = job_repo or JobRepository()

    @property
    def history_repo(self) -> JobStatusHistoryRepository:
        return cast(JobStatusHistoryRepository, self.repository)

    def _validate_job(self, session: Session, job_id: int) -> None:
        if self._job_repo.get(session, job_id) is None:
            raise EntityNotFoundError("Job not found")

    def create_history(
        self, session: Session, job_id: int, data: JobStatusHistoryCreate
    ) -> JobStatusHistory:
        self._validate_job(session, job_id)
        history = JobStatusHistory(job_id=job_id, **data.model_dump())
        return self.create(session, history)

    def update_history(
        self,
        session: Session,
        history: JobStatusHistory,
        data: JobStatusHistoryUpdate,
    ) -> JobStatusHistory:
        values = data.model_dump(exclude_unset=True)
        if "job_id" in values and values["job_id"] is not None:
            self._validate_job(session, values["job_id"])
        return self.update(session, history, values)
