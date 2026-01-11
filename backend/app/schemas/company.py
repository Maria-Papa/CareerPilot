from app.schemas.base import ORMBase, SoftDeleteRead, TimestampRead


class CompanyBase(ORMBase):
    name: str
    logo_url: str | None = None
    website: str | None = None
    industry: str | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(ORMBase):
    name: str | None = None
    logo_url: str | None = None
    website: str | None = None
    industry: str | None = None


class CompanyRead(CompanyBase, TimestampRead, SoftDeleteRead):
    id: int

    class Config:
        from_attributes = True
