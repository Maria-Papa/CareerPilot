from datetime import datetime

from app.schemas.base import ORMBase, SoftDeleteRead, TimestampRead
from pydantic import EmailStr


class UserBase(ORMBase):
    email: EmailStr
    is_active: bool = True
    is_verified: bool = False


class UserCreate(UserBase):
    password: str


class UserUpdate(ORMBase):
    email: EmailStr | None = None
    is_active: bool | None = None
    is_verified: bool | None = None
    password: str | None = None


class UserRead(UserBase, TimestampRead, SoftDeleteRead):
    id: int
    last_login_at: datetime | None
