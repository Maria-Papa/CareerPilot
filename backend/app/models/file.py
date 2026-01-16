from __future__ import annotations

from typing import TYPE_CHECKING

from app.db.base import BaseModel
from app.enums import FileType
from app.models.mixins import SoftDeleteMixin, TimestampMixin
from sqlalchemy import Enum, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models import JobFileAttachment, User


class File(BaseModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "files"
    __table_args__ = (
        Index("idx_files_user_id", "user_id"),
        Index("idx_files_file_type", "file_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    file_url: Mapped[str] = mapped_column(String(512))
    file_type: Mapped[FileType] = mapped_column(
        Enum(FileType, name="file_type_enum", native_enum=False, validate_strings=True),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="files")
    attachments: Mapped[list["JobFileAttachment"]] = relationship(
        back_populates="file",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"File(id={self.id!r}, user_id={self.user_id!r}, file_type={self.file_type!r})"
