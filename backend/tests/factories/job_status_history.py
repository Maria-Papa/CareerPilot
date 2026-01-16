from datetime import datetime, timezone

from app.enums.job_status import JobStatus
from app.models.job_status_history import JobStatusHistory
from sqlalchemy.orm import Session


def create_job_status_history(db_session: Session, **kwargs) -> JobStatusHistory:
    if "job_id" not in kwargs:
        raise ValueError("JobStatusHistory factory requires job_id")

    defaults = {
        "status": JobStatus.APPLIED,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    defaults.update(kwargs)

    history = JobStatusHistory(**defaults)
    db_session.add(history)
    db_session.commit()
    db_session.refresh(history)
    return history
