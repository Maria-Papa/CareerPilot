from pydantic import BaseModel
from app.schemas import TimestampRead


class CurrencyBase(BaseModel):
    code: str
    symbol: str | None = None


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyUpdate(BaseModel):
    code: str | None = None
    symbol: str | None = None


class CurrencyRead(CurrencyBase, TimestampRead):
    id: int

    class Config:
        from_attributes = True
