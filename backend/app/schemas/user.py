from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.schemas import TimestampRead, SoftDeleteRead


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    is_verified: bool = False


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = None
    is_verified: bool | None = None
    password: str | None = None


class UserRead(UserBase, TimestampRead, SoftDeleteRead):
    id: int
    last_login_at: datetime | None

    class Config:
        from_attributes = True
