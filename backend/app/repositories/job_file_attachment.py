from datetime import datetime
from sqlalchemy.orm import Session

from app.models import JobFileAttachment
from app.repositories import BaseRepository


class JobFileAttachmentRepository(BaseRepository[JobFileAttachment]):
    def __init__(self):
        super().__init__(JobFileAttachment)

    def detach(self, db: Session, attachment: JobFileAttachment) -> JobFileAttachment:
        try:
            attachment.detached_at = datetime.utcnow()
            attachment.is_active = False
            db.commit()
            db.refresh(attachment)
            return attachment
        except Exception:
            db.rollback()
            raise
