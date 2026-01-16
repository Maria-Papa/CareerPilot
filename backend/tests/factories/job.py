from datetime import datetime, timezone

from app.enums.job_status import JobStatus
from app.models.job import Job
from sqlalchemy.orm import Session


def create_job(db_session: Session, **kwargs) -> Job:
    if "user_id" not in kwargs:
        raise ValueError("Job factory requires user_id")
    if "company_id" not in kwargs:
        raise ValueError("Job factory requires company_id")

    defaults = {
        "location_id": None,
        "title": "Test Job",
        "employment_type": None,
        "flexibility": None,
        "description_html": None,
        "description_text": None,
        "job_url": None,
        "salary_gross_given": None,
        "salary_gross_calculated": None,
        "salary_net": None,
        "current_status": JobStatus.APPLIED,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    defaults.update(kwargs)

    job = Job(**defaults)
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)
    return job
