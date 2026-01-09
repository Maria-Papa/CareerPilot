from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models import JobFileAttachment
from app.repositories import SoftDeleteBaseRepository


class JobFileAttachmentRepository(SoftDeleteBaseRepository[JobFileAttachment]):
    def __init__(self):
        super().__init__(JobFileAttachment)
