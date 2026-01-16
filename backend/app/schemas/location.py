from app.schemas.base import ORMBase, TimestampRead


class LocationBase(ORMBase):
    name: str
    country_code: str
    currency_id: int


class LocationCreate(LocationBase):
    pass


class LocationUpdate(ORMBase):
    name: str | None = None
    country_code: str | None = None
    currency_id: int | None = None


class LocationRead(LocationBase, TimestampRead):
    id: int
