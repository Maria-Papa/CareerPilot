from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models import Interview
from app.repositories import InterviewRepository
from app.schemas import InterviewCreate, InterviewUpdate
from app.services import BaseService


class InterviewService(BaseService[Interview]):
    repository: InterviewRepository

    def __init__(self):
        super().__init__(InterviewRepository())

    def create_interview(self, session: Session, data: InterviewCreate) -> Interview:
        interview = Interview(**data.model_dump())
        interview.created_at = datetime.now(timezone.utc)
        return self.create(session, interview)

    def update_interview(
        self, session: Session, interview: Interview, data: InterviewUpdate
    ) -> Interview:
        values = data.model_dump(exclude_unset=True)
        return self.update(session, interview, values)

    def reschedule(
        self, session: Session, interview: Interview, new_time: datetime
    ) -> Interview:
        interview.scheduled_at = new_time
        session.commit()
        session.refresh(interview)
        return interview
