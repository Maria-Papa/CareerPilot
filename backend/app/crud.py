from sqlalchemy.orm import Session
from . import models, schemas


def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.JobApplication(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def get_jobs(db: Session):
    return db.query(models.JobApplication).all()


def get_job(db: Session, job_id: int):
    return (
        db.query(models.JobApplication)
        .filter(models.JobApplication.id == job_id)
        .first()
    )


def update_job(db: Session, job_id: int, job_update: schemas.JobUpdate):
    db_job = get_job(db, job_id)
    if not db_job:
        return None

    for key, value in job_update.dict(exclude_unset=True).items():
        setattr(db_job, key, value)

    db.commit()
    db.refresh(db_job)
    return db_job


def delete_job(db: Session, job_id: int):
    db_job = get_job(db, job_id)
    if not db_job:
        return None

    db.delete(db_job)
    db.commit()
    return True
