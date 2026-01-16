from datetime import datetime

from app.enums import InterviewOutcome, InterviewType
from app.schemas.base import ORMBase, TimestampRead


class InterviewBase(ORMBase):
    interview_type: InterviewType
    scheduled_at: datetime | None = None
    outcome: InterviewOutcome | None = None
    notes: str | None = None


class InterviewCreate(InterviewBase):
    pass


class InterviewUpdate(ORMBase):
    interview_type: InterviewType | None = None
    scheduled_at: datetime | None = None
    outcome: InterviewOutcome | None = None
    notes: str | None = None


class InterviewRead(InterviewBase, TimestampRead):
    id: int
    job_id: int
