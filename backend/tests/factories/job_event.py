from datetime import datetime, timezone

from app.enums.job_event_type import JobEventType
from app.models.job_event import JobEvent
from sqlalchemy.orm import Session


def create_job_event(db_session: Session, **kwargs) -> JobEvent:
    if "job_id" not in kwargs:
        raise ValueError("JobEvent factory requires job_id")

    defaults = {
        "event_type": JobEventType.APPLICATION_SUBMITTED,
        "payload": None,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    defaults.update(kwargs)

    event = JobEvent(**defaults)
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)
    return event
