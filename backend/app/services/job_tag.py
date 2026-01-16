from typing import cast

from app.core.errors import EntityNotFoundError
from app.models import JobTag
from app.repositories import JobRepository, JobTagRepository, TagRepository
from app.schemas import JobTagCreate, JobTagUpdate
from app.services import BaseService
from sqlalchemy.orm import Session


class JobTagService(BaseService[JobTag]):
    def __init__(
        self,
        repository: JobTagRepository | None = None,
        job_repo: JobRepository | None = None,
        tag_repo: TagRepository | None = None,
    ) -> None:
        repository = repository or JobTagRepository()
        super().__init__(repository)
        self._job_repo = job_repo or JobRepository()
        self._tag_repo = tag_repo or TagRepository()

    @property
    def tag_repo(self) -> JobTagRepository:
        return cast(JobTagRepository, self.repository)

    def _validate_job(self, session: Session, job_id: int) -> None:
        if self._job_repo.get(session, job_id) is None:
            raise EntityNotFoundError("Job not found")

    def _validate_tag(self, session: Session, tag_id: int) -> None:
        if self._tag_repo.get(session, tag_id) is None:
            raise EntityNotFoundError("Tag not found")

    def get_link(self, session: Session, job_id: int, tag_id: int) -> JobTag | None:
        return self.repository.find_one(session, job_id=job_id, tag_id=tag_id)

    def create_tag(self, session: Session, job_id: int, data: JobTagCreate) -> JobTag:
        self._validate_job(session, job_id)
        self._validate_tag(session, data.tag_id)

        link = JobTag(job_id=job_id, tag_id=data.tag_id)
        return self.create(session, link)

    def update_tag(
        self,
        session: Session,
        link: JobTag,
        data: JobTagUpdate,
    ) -> JobTag:
        values = data.model_dump(exclude_unset=True)

        if "tag_id" in values and values["tag_id"] is not None:
            self._validate_tag(session, values["tag_id"])

        return self.update(session, link, values)
