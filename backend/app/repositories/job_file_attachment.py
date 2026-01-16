from app.models.job_file_attachment import JobFileAttachment
from app.repositories.soft_delete_base import SoftDeleteBaseRepository


class JobFileAttachmentRepository(SoftDeleteBaseRepository[JobFileAttachment]):
    def __init__(self):
        super().__init__(JobFileAttachment)
