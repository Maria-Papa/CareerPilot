from sqlalchemy.orm import Session
from app.models import Tag
from app.repositories import TagRepository
from app.schemas import TagCreate, TagUpdate
from app.services import BaseService


class TagService(BaseService[Tag]):
    repository: TagRepository

    def __init__(self):
        super().__init__(TagRepository())

    def create_tag(self, session: Session, data: TagCreate) -> Tag:
        tag = Tag(**data.model_dump())
        return self.create(session, tag)

    def update_tag(self, session: Session, tag: Tag, data: TagUpdate) -> Tag:
        values = data.model_dump(exclude_unset=True)
        return self.update(session, tag, values)
