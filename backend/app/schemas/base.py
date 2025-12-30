from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TimestampRead(ORMBase):
    created_at: datetime
    updated_at: datetime


class SoftDeleteRead(ORMBase):
    deleted_at: datetime | None
