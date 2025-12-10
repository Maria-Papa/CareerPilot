# backend/app/repositories/job_repo.py
from sqlalchemy.orm import Session
from app.models import JobApplication
from typing import List, Optional

def create(db: Session, payload: dict) -> JobApplication:
    job = JobApplication(**payload)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def list_all(db: Session) -> List[JobApplication]:
    return db.query(JobApplication).order_by(JobApplication.created_at.desc()).all()

def get(db: Session, job_id: int) -> Optional[JobApplication]:
    return db.query(JobApplication).filter(JobApplication.id == job_id).first()

def update(db: Session, job: JobApplication, data: dict) -> JobApplication:
    for k, v in data.items():
        setattr(job, k, v)
    db.commit()
    db.refresh(job)
    return job

def delete(db: Session, job: JobApplication):
    db.delete(job)
    db.commit()
