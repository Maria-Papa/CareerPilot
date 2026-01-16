from datetime import datetime, timezone

from app.enums.interview_type import InterviewType
from app.models.interview import Interview
from sqlalchemy.orm import Session


def create_interview(db_session: Session, **kwargs) -> Interview:
    if "job_id" not in kwargs:
        raise ValueError("Interview factory requires job_id")

    defaults = {
        "interview_type": InterviewType.HR_SCREEN,
        "scheduled_at": datetime.now(timezone.utc),
        "outcome": None,
        "notes": None,
    }
    defaults.update(kwargs)

    interview = Interview(**defaults)
    db_session.add(interview)
    db_session.commit()
    db_session.refresh(interview)
    return interview
