# backend/app/services/job_service.py
from sqlalchemy.orm import Session
from app.repositories.job_repo import create, list_all, get, update, delete


def create_job(db: Session, job_data: dict):
    job_data.setdefault("status", "saved")
    return create(db, job_data)


def get_jobs(db: Session):
    return list_all(db)


def get_job(db: Session, job_id: int):
    return get(db, job_id)


def update_job_service(db: Session, job_id: int, update_data: dict):
    job = get(db, job_id)
    if not job:
        return None

    # business rule example
    if update_data.get("status") == "rejected" and not job.rejection_date:
        update_data.setdefault("rejection_date", None)

    return update(db, job, update_data)


def delete_job_service(db: Session, job_id: int):
    job = get(db, job_id)
    if not job:
        return False

    delete(db, job)
    return True
