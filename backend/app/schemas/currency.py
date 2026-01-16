from app.schemas.base import ORMBase, TimestampRead
from pydantic import Field


class CurrencyBase(ORMBase):
    code: str = Field(..., min_length=2, max_length=3)
    symbol: str | None = Field(None, max_length=5)


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyUpdate(ORMBase):
    code: str | None = Field(None, min_length=2, max_length=3)
    symbol: str | None = Field(None, max_length=5)


class CurrencyRead(CurrencyBase, TimestampRead):
    id: int
