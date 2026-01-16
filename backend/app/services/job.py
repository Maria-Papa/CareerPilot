from datetime import datetime, timezone
from typing import cast

from app.core.errors import EntityNotFoundError, InvalidStateTransitionError
from app.enums.job_status import JobStatus
from app.models.job import Job
from app.models.job_file_attachment import JobFileAttachment
from app.models.job_status_history import JobStatusHistory
from app.repositories.company import CompanyRepository
from app.repositories.job import JobRepository
from app.repositories.location import LocationRepository
from app.repositories.user import UserRepository
from app.schemas.job import JobCreate, JobUpdate
from app.services.soft_delete_base import SoftDeleteService
from sqlalchemy.orm import Session


class JobService(SoftDeleteService[Job]):
    def __init__(
        self,
        repository: JobRepository | None = None,
        user_repo: UserRepository | None = None,
        company_repo: CompanyRepository | None = None,
        location_repo: LocationRepository | None = None,
    ) -> None:
        super().__init__(repository or JobRepository())
        self.user_repo = user_repo or UserRepository()
        self.company_repo = company_repo or CompanyRepository()
        self.location_repo = location_repo or LocationRepository()

    @property
    def job_repo(self) -> JobRepository:
        return cast(JobRepository, self.repository)

    def _validate_user(self, session: Session, user_id: int) -> None:
        if self.user_repo.get(session, user_id) is None:
            raise EntityNotFoundError("User not found")

    def _validate_company(self, session: Session, company_id: int) -> None:
        if self.company_repo.get(session, company_id) is None:
            raise EntityNotFoundError("Company not found")

    def _validate_location(self, session: Session, location_id: int | None) -> None:
        if (
            location_id is not None
            and self.location_repo.get(session, location_id) is None
        ):
            raise EntityNotFoundError("Location not found")

    def get_for_user(self, session: Session, job_id: int, user_id: int) -> Job:
        job = self.job_repo.get_for_user(session, job_id, user_id)
        if job is None:
            raise EntityNotFoundError("Job not found or not owned by user")
        return job

    def get_including_deleted_for_user(
        self, session: Session, job_id: int, user_id: int
    ) -> Job:
        job = self.job_repo.get_including_deleted(session, job_id)
        if job is None or job.user_id != user_id:
            raise EntityNotFoundError("Job not found or not owned by user")
        return job

    def list_for_user(
        self, session: Session, user_id: int, *, offset: int = 0, limit: int = 100
    ):
        return self.job_repo.list_for_user(session, user_id, offset=offset, limit=limit)

    def create_job(self, session: Session, data: JobCreate, user_id: int) -> Job:
        self._validate_user(session, user_id)
        self._validate_company(session, data.company_id)
        self._validate_location(session, data.location_id)

        job = Job(**data.model_dump(exclude={"user_id"}), user_id=user_id)
        return self.create(session, job)

    def update_job(self, session: Session, job: Job, data: JobUpdate) -> Job:
        values = data.model_dump(exclude_unset=True)

        if "user_id" in values:
            values.pop("user_id", None)

        if "company_id" in values:
            self._validate_company(session, values["company_id"])
        if "location_id" in values:
            self._validate_location(session, values["location_id"])

        return self.update(session, job, values)

    def change_status(self, session: Session, job: Job, new_status: JobStatus) -> Job:
        if job.current_status == JobStatus.REJECTED:
            raise InvalidStateTransitionError("Cannot change status after rejection")

        history = JobStatusHistory(
            job_id=job.id,
            status=new_status,
        )
        self.job_repo.add_status_history(session, history)

        job.current_status = new_status
        session.commit()
        session.refresh(job)
        return job

    def attach_file(
        self,
        session: Session,
        job: Job,
        file_id: int,
        version: int,
    ) -> JobFileAttachment:
        attachment = JobFileAttachment(
            job_id=job.id,
            file_id=file_id,
            version=version,
            is_active=True,
            attached_at=datetime.now(timezone.utc),
        )
        return self.job_repo.add_file_attachment(session, attachment)
