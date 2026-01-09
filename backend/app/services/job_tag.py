from sqlalchemy.orm import Session
from app.models import JobTag
from app.repositories import JobTagRepository
from app.services import BaseService
from app.schemas import JobTagCreate, JobTagUpdate


class JobTagService(BaseService[JobTag]):
    repository: JobTagRepository

    def __init__(self):
        super().__init__(JobTagRepository())

    def create_tag(self, session: Session, data: JobTagCreate) -> JobTag:
        tag = JobTag(**data.model_dump())
        return self.create(session, tag)

    def update_tag(self, session: Session, tag: JobTag, data: JobTagUpdate) -> JobTag:
        values = data.model_dump(exclude_unset=True)
        return self.update(session, tag, values)
