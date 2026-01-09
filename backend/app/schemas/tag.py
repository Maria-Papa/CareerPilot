from pydantic import BaseModel
from app.schemas import TimestampRead, SoftDeleteRead


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: str | None = None


class TagRead(TagBase, TimestampRead, SoftDeleteRead):
    id: int

    class Config:
        from_attributes = True
