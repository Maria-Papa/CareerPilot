from sqlalchemy.orm import Session
from app.models import JobEvent
from app.repositories import JobEventRepository
from app.services import BaseService
from app.schemas import JobEventCreate, JobEventUpdate


class JobEventService(BaseService[JobEvent]):
    repository: JobEventRepository

    def __init__(self):
        super().__init__(JobEventRepository())

    def create_job_event(self, session: Session, data: JobEventCreate) -> JobEvent:
        event = JobEvent(**data.model_dump())
        return self.create(session, event)

    def update_job_event(
        self, session: Session, event: JobEvent, data: JobEventUpdate
    ) -> JobEvent:
        values = data.model_dump(exclude_unset=True)
        return self.update(session, event, values)

    def add_payload_data(
        self, session: Session, event: JobEvent, extra_payload: dict
    ) -> JobEvent:
        if not event.payload:
            event.payload = {}
        event.payload.update(extra_payload)
        return self.update(session, event, {"payload": event.payload})
