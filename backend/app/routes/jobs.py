from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.job_service import (
    create_job,
    get_jobs,
    get_job,
    update_job_service,
    delete_job_service,
)
from app import schemas
from app.database import get_db

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/", response_model=schemas.Job)
def create_job_route(job: schemas.JobCreate, db: Session = Depends(get_db)):
    return create_job(db=db, job_data=job.dict())


@router.get("/", response_model=list[schemas.Job])
def list_jobs_route(db: Session = Depends(get_db)):
    return get_jobs(db)


@router.get("/{job_id}", response_model=schemas.Job)
def get_job_route(job_id: int, db: Session = Depends(get_db)):
    db_job = get_job(db, job_id)
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job


@router.put("/{job_id}", response_model=schemas.Job)
def update_job_route(
    job_id: int, job_update: schemas.JobUpdate, db: Session = Depends(get_db)
):
    updated = update_job_service(db, job_id, job_update.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Job not found")
    return updated


@router.delete("/{job_id}")
def delete_job_route(job_id: int, db: Session = Depends(get_db)):
    success = delete_job_service(db, job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"detail": "Job deleted"}
