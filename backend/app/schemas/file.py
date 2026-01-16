from app.enums.file_type import FileType
from app.schemas.base import ORMBase, SoftDeleteRead, TimestampRead


class FileBase(ORMBase):
    user_id: int
    file_url: str
    file_type: FileType


class FileCreate(FileBase):
    pass


class FileUpdate(ORMBase):
    user_id: int | None = None
    file_url: str | None = None
    file_type: FileType | None = None


class FileRead(FileBase, TimestampRead, SoftDeleteRead):
    id: int
