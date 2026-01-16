from datetime import datetime, timezone

from app.models.job_file_attachment import JobFileAttachment
from sqlalchemy.orm import Session


def create_job_file_attachment(db_session: Session, **kwargs) -> JobFileAttachment:
    if "job_id" not in kwargs:
        raise ValueError("JobFileAttachment factory requires job_id")
    if "file_id" not in kwargs:
        raise ValueError("JobFileAttachment factory requires file_id")

    job_id = kwargs["job_id"]
    file_id = kwargs["file_id"]

    if "version" not in kwargs:
        last = (
            db_session.query(JobFileAttachment)
            .filter_by(job_id=job_id, file_id=file_id)
            .order_by(JobFileAttachment.version.desc())
            .first()
        )
        kwargs["version"] = 1 if last is None else last.version + 1

    defaults = {
        "is_active": True,
        "attached_at": datetime.now(timezone.utc),
        "detached_at": None,
    }
    defaults.update(kwargs)

    attachment = JobFileAttachment(**defaults)
    db_session.add(attachment)
    db_session.commit()
    db_session.refresh(attachment)
    return attachment
