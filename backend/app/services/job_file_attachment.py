from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models import JobFileAttachment
from app.repositories import JobFileAttachmentRepository
from app.services import BaseService
from app.schemas import JobFileAttachmentCreate, JobFileAttachmentUpdate


class JobFileAttachmentService(BaseService[JobFileAttachment]):
    repository: JobFileAttachmentRepository

    def __init__(self):
        super().__init__(JobFileAttachmentRepository())

    def create_attachment(
        self, session: Session, data: JobFileAttachmentCreate
    ) -> JobFileAttachment:
        attachment = JobFileAttachment(**data.model_dump())
        return self.create(session, attachment)

    def update_attachment(
        self,
        session: Session,
        attachment: JobFileAttachment,
        data: JobFileAttachmentUpdate,
    ) -> JobFileAttachment:
        values = data.model_dump(exclude_unset=True)
        return self.update(session, attachment, values)

    def detach_attachment(
        self, session: Session, attachment: JobFileAttachment
    ) -> JobFileAttachment:
        attachment.detached_at = datetime.now(timezone.utc)
        attachment.is_active = False
        session.commit()
        session.refresh(attachment)
        return attachment
