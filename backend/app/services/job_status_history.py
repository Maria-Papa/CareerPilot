from sqlalchemy.orm import Session
from app.models import JobStatusHistory
from app.repositories import JobStatusHistoryRepository
from app.schemas import JobStatusHistoryCreate, JobStatusHistoryUpdate
from app.services import BaseService


class JobStatusHistoryService(BaseService[JobStatusHistory]):
    repository: JobStatusHistoryRepository

    def __init__(self):
        super().__init__(JobStatusHistoryRepository())

    def create_history(
        self, session: Session, data: JobStatusHistoryCreate
    ) -> JobStatusHistory:
        history = JobStatusHistory(**data.model_dump())
        return self.create(session, history)

    def update_history(
        self, session: Session, history: JobStatusHistory, data: JobStatusHistoryUpdate
    ) -> JobStatusHistory:
        values = data.model_dump(exclude_unset=True)
        return self.update(session, history, values)
