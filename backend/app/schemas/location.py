from pydantic import BaseModel
from app.schemas import TimestampRead, SoftDeleteRead


class LocationBase(BaseModel):
    name: str
    country_code: str
    currency_id: int


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: str | None = None
    country_code: str | None = None
    currency_id: int | None = None


class LocationRead(LocationBase, TimestampRead, SoftDeleteRead):
    id: int

    class Config:
        from_attributes = True
