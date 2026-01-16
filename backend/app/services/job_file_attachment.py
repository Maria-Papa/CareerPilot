from datetime import datetime, timezone
from typing import cast

from app.core.errors import EntityNotFoundError
from app.models.job_file_attachment import JobFileAttachment
from app.repositories import JobFileAttachmentRepository, JobRepository
from app.schemas import JobFileAttachmentCreate, JobFileAttachmentUpdate
from app.services.soft_delete_base import SoftDeleteService
from sqlalchemy.orm import Session


class JobFileAttachmentService(SoftDeleteService[JobFileAttachment]):
    def __init__(
        self,
        repository: JobFileAttachmentRepository | None = None,
        job_repo: JobRepository | None = None,
    ) -> None:
        repository = repository or JobFileAttachmentRepository()
        super().__init__(repository)
        self._job_repo = job_repo or JobRepository()

    @property
    def attachment_repo(self) -> JobFileAttachmentRepository:
        return cast(JobFileAttachmentRepository, self.repository)

    def _validate_job(self, session: Session, job_id: int) -> None:
        if self._job_repo.get(session, job_id) is None:
            raise EntityNotFoundError("Job not found")

    def create_attachment(
        self, session: Session, job_id: int, data: JobFileAttachmentCreate
    ) -> JobFileAttachment:
        self._validate_job(session, job_id)
        values = data.model_dump()
        values["job_id"] = job_id
        attachment = JobFileAttachment(**values)
        return self.create(session, attachment)

    def update_attachment(
        self,
        session: Session,
        attachment: JobFileAttachment,
        data: JobFileAttachmentUpdate,
    ) -> JobFileAttachment:
        values = data.model_dump(exclude_unset=True)

        if "job_id" in values and values["job_id"] is not None:
            self._validate_job(session, values["job_id"])

        return self.update(session, attachment, values)

    def detach_attachment(
        self, session: Session, attachment: JobFileAttachment
    ) -> JobFileAttachment:
        values = {
            "detached_at": datetime.now(timezone.utc),
            "is_active": False,
        }
        return self.update(session, attachment, values)
