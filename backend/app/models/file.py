from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import (
    Index,
    String,
    ForeignKey,
    DateTime,
    SmallInteger,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.enums import FileType
from app.models import Base

if TYPE_CHECKING:
    from app.models import User


class File(Base):
    __tablename__ = "files"
    __table_args__ = (
        Index("idx_files_user_id", "user_id"),
        Index("idx_files_file_type", "file_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    file_url: Mapped[str] = mapped_column(String(512))
    file_type: Mapped[FileType] = mapped_column(SmallInteger)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="files")
