from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import (
    Enum,
    Index,
    String,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.enums import FileType
from app.models import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models import User


class File(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "files"
    __table_args__ = (
        Index("idx_files_user_id", "user_id"),
        Index("idx_files_file_type", "file_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    file_url: Mapped[str] = mapped_column(String(512))
    file_type: Mapped[FileType] = mapped_column(
        Enum(
            FileType,
            name="file_type_enum",
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="files")
