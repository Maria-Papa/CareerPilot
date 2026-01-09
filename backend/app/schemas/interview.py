from datetime import datetime
from pydantic import BaseModel
from app.enums import InterviewType, InterviewOutcome
from app.schemas import TimestampRead, SoftDeleteRead


class InterviewBase(BaseModel):
    job_id: int
    interview_type: InterviewType
    scheduled_at: datetime | None = None
    outcome: InterviewOutcome | None = None
    notes: str | None = None


class InterviewCreate(InterviewBase):
    pass


class InterviewUpdate(BaseModel):
    job_id: int | None = None
    interview_type: InterviewType | None = None
    scheduled_at: datetime | None = None
    outcome: InterviewOutcome | None = None
    notes: str | None = None


class InterviewRead(InterviewBase, TimestampRead, SoftDeleteRead):
    id: int

    class Config:
        from_attributes = True
