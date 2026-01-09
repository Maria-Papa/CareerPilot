from pydantic import BaseModel, Field
from app.schemas import TimestampRead


class CostOfLivingBase(BaseModel):
    location_id: int
    yearly_cost: int = Field(..., description="Yearly cost in cents")
    title: str | None = Field(None, max_length=100)


class CostOfLivingCreate(CostOfLivingBase):
    pass


class CostOfLivingUpdate(BaseModel):
    location_id: int | None = None
    yearly_cost: int | None = None
    title: str | None = None


class CostOfLivingRead(CostOfLivingBase, TimestampRead):
    id: int

    class Config:
        from_attributes = True
