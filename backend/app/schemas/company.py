from pydantic import BaseModel
from app.schemas import TimestampRead, SoftDeleteRead


class CompanyBase(BaseModel):
    name: str
    logo_url: str | None = None
    website: str | None = None
    industry: str | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = None
    logo_url: str | None = None
    website: str | None = None
    industry: str | None = None


class CompanyRead(CompanyBase, TimestampRead, SoftDeleteRead):
    id: int

    class Config:
        from_attributes = True
