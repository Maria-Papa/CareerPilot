from pydantic import BaseModel
from .base import TimestampRead, SoftDeleteRead


class CurrencyBase(BaseModel):
    code: str
    symbol: str | None = None


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyUpdate(BaseModel):
    code: str | None = None
    symbol: str | None = None


class CurrencyRead(CurrencyBase, TimestampRead, SoftDeleteRead):
    id: int

    class Config:
        from_attributes = True
