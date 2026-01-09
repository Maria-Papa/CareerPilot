from pydantic import BaseModel
from app.enums import FileType
from app.schemas import TimestampRead, SoftDeleteRead


class FileBase(BaseModel):
    user_id: int
    file_url: str
    file_type: FileType


class FileCreate(FileBase):
    pass


class FileUpdate(BaseModel):
    user_id: int | None = None
    file_url: str | None = None
    file_type: FileType | None = None


class FileRead(FileBase, TimestampRead, SoftDeleteRead):
    id: int

    class Config:
        from_attributes = True
