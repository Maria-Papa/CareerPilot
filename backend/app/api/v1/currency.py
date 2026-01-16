from app.api.deps import get_entity_or_404
from app.db import get_session
from app.models.currency import Currency
from app.schemas.currency import CurrencyCreate, CurrencyRead, CurrencyUpdate
from app.services.currency import CurrencyService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/currencies", tags=["currencies"])

service = CurrencyService()
get_currency_or_404 = get_entity_or_404(service.get_currency)


@router.get("", response_model=list[CurrencyRead])
def list_currencies(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    return service.list_currencies(session, offset=offset, limit=limit)


@router.get("/{currency_id}", response_model=CurrencyRead)
def get_currency(currency: Currency = Depends(get_currency_or_404)):
    return currency


@router.post("", response_model=CurrencyRead, status_code=status.HTTP_201_CREATED)
def create_currency(data: CurrencyCreate, session: Session = Depends(get_session)):
    return service.create_currency(session, data)


@router.patch("/{currency_id}", response_model=CurrencyRead)
def update_currency(
    data: CurrencyUpdate,
    currency: Currency = Depends(get_currency_or_404),
    session: Session = Depends(get_session),
):
    return service.update_currency(session, currency, data)


@router.delete("/{currency_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_currency(
    currency: Currency = Depends(get_currency_or_404),
    session: Session = Depends(get_session),
):
    service.delete(session, currency)
    return None
