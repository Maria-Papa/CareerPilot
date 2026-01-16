from typing import Optional, Sequence

from app.core.error_handlers import EntityNotFoundError
from app.models.tag import Tag
from app.repositories.tag import TagRepository
from app.schemas.tag import TagCreate, TagUpdate
from app.services.base import BaseService
from sqlalchemy.orm import Session


class TagService(BaseService[Tag]):
    def __init__(self, repository: Optional[TagRepository] = None):
        repository = repository or TagRepository()
        super().__init__(repository)

    def list_tags(
        self, session: Session, *, offset: int = 0, limit: int = 100
    ) -> Sequence[Tag]:
        return self.list(session, offset=offset, limit=limit)

    def get_tag(self, session: Session, id: int) -> Tag:
        tag = self.repository.get(session, id)
        if tag is None:
            raise EntityNotFoundError("Tag not found")
        return tag

    def create_tag(self, session: Session, data: TagCreate) -> Tag:
        tag = Tag(**data.model_dump())
        return self.create(session, tag)

    def update_tag(self, session: Session, tag: Tag, data: TagUpdate) -> Tag:
        values = data.model_dump(exclude_unset=True)
        return self.update(session, tag, values)

    def delete_tag(self, session: Session, tag: Tag) -> None:
        self.delete(session, tag)
