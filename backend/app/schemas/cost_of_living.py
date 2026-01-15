from app.schemas.base import ORMBase, TimestampRead
from pydantic import Field


class CostOfLivingBase(ORMBase):
    location_id: int
    yearly_cost: int = Field(..., description="Yearly cost in cents")
    title: str | None = Field(None, max_length=100)


class CostOfLivingCreate(CostOfLivingBase):
    pass


class CostOfLivingUpdate(ORMBase):
    location_id: int | None = None
    yearly_cost: int | None = None
    title: str | None = None


class CostOfLivingRead(CostOfLivingBase, TimestampRead):
    id: int
