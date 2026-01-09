from app.models import Job, JobStatusHistory, JobFileAttachment
from app.repositories import SoftDeleteBaseRepository


class JobRepository(SoftDeleteBaseRepository[Job]):
    def __init__(self):
        super().__init__(Job)
