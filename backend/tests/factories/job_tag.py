from app.models.job_tag import JobTag
from sqlalchemy.orm import Session


def create_job_tag(db_session: Session, **kwargs) -> JobTag:
    if "job_id" not in kwargs or "tag_id" not in kwargs:
        raise ValueError("JobTag factory requires job_id and tag_id")

    tag_link = JobTag(**kwargs)
    db_session.add(tag_link)
    db_session.commit()
    db_session.refresh(tag_link)
    return tag_link
