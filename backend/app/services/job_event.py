from typing import Sequence, cast

from app.core.error_handlers import EntityNotFoundError
from app.models.job_event import JobEvent
from app.repositories.job import JobRepository
from app.repositories.job_event import JobEventRepository
from app.schemas.job_event import JobEventCreate, JobEventUpdate
from app.services.base import BaseService
from sqlalchemy.orm import Session


class JobEventService(BaseService[JobEvent]):
    def __init__(
        self,
        repository: JobEventRepository | None = None,
        job_repo: JobRepository | None = None,
    ) -> None:
        repository = repository or JobEventRepository()
        super().__init__(repository)
        self._job_repo = job_repo or JobRepository()

    @property
    def job_event_repo(self) -> JobEventRepository:
        return cast(JobEventRepository, self.repository)

    def _validate_job(self, session: Session, job_id: int) -> None:
        if self._job_repo.get(session, job_id) is None:
            raise EntityNotFoundError("Job not found")

    def list_for_job(
        self, session: Session, job_id: int, *, offset: int = 0, limit: int = 100
    ) -> Sequence[JobEvent]:
        return self.find(session, job_id=job_id)[offset : offset + limit]

    def get_job_event(self, session: Session, id: int) -> JobEvent:
        event = self.repository.get(session, id)
        if event is None:
            raise EntityNotFoundError("JobEvent not found")
        return event

    def create_for_job(
        self, session: Session, job_id: int, data: JobEventCreate
    ) -> JobEvent:
        self._validate_job(session, job_id)

        event = JobEvent(
            job_id=job_id,
            event_type=data.event_type,
            payload=data.payload,
        )
        return self.create(session, event)

    def update_for_job(
        self,
        session: Session,
        event: JobEvent,
        job_id: int,
        data: JobEventUpdate,
    ) -> JobEvent:
        self._validate_job(session, job_id)

        values = data.model_dump(exclude_unset=True)
        values["job_id"] = job_id

        return self.update(session, event, values)

    def add_payload_data(
        self, session: Session, event: JobEvent, extra_payload: dict
    ) -> JobEvent:
        payload = event.payload or {}
        payload.update(extra_payload)
        return self.update(session, event, {"payload": payload})
