from typing import Sequence

from app.api.deps import get_entity_or_404
from app.db import get_session
from app.models.cost_of_living import CostOfLiving
from app.schemas.cost_of_living import (
    CostOfLivingCreate,
    CostOfLivingRead,
    CostOfLivingUpdate,
)
from app.services.cost_of_living import CostOfLivingService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/cost-of-living", tags=["cost_of_living"])

service = CostOfLivingService()
get_cost_or_404 = get_entity_or_404(service.get_cost)


@router.get("", response_model=list[CostOfLivingRead])
def list_costs(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
) -> Sequence[CostOfLiving]:
    return service.list_costs(session, offset=offset, limit=limit)


@router.get("/{col_id}", response_model=CostOfLivingRead)
def get_cost(col: CostOfLiving = Depends(get_cost_or_404)):
    return col


@router.post("", response_model=CostOfLivingRead, status_code=status.HTTP_201_CREATED)
def create_cost(data: CostOfLivingCreate, session: Session = Depends(get_session)):
    return service.create_cost(session, data)


@router.patch("/{col_id}", response_model=CostOfLivingRead)
def update_cost(
    data: CostOfLivingUpdate,
    col: CostOfLiving = Depends(get_cost_or_404),
    session: Session = Depends(get_session),
):
    return service.update_cost(session, col, data)


@router.delete("/{col_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cost(
    col: CostOfLiving = Depends(get_cost_or_404),
    session: Session = Depends(get_session),
):
    service.delete(session, col)
    return None
