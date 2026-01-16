from app.schemas.base import ORMBase, TimestampRead


class TagBase(ORMBase):
    name: str


class TagCreate(TagBase):
    pass


class TagUpdate(ORMBase):
    name: str | None = None


class TagRead(TagBase, TimestampRead):
    id: int
