from typing import Optional, Sequence

from app.core.errors import ConflictError, EntityNotFoundError
from app.models.currency import Currency
from app.repositories.currency import CurrencyRepository
from app.schemas.currency import CurrencyCreate, CurrencyUpdate
from app.services.base import BaseService
from sqlalchemy.orm import Session


class CurrencyService(BaseService[Currency]):
    def __init__(self, repository: Optional[CurrencyRepository] = None) -> None:
        repository = repository or CurrencyRepository()
        super().__init__(repository)

    def list_currencies(
        self, session: Session, *, offset: int = 0, limit: int = 100
    ) -> Sequence[Currency]:
        return self.list(session, offset=offset, limit=limit)

    def get_currency(self, session: Session, id: int) -> Currency:
        currency = self.get(session, id)
        if currency is None:
            raise EntityNotFoundError("Currency not found")
        return currency

    def create_currency(self, session: Session, data: CurrencyCreate) -> Currency:
        if self.find_one(session, code=data.code) is not None:
            raise ConflictError("Currency code already exists")
        currency = Currency(**data.model_dump())
        return self.create(session, currency)

    def update_currency(
        self, session: Session, currency: Currency, data: CurrencyUpdate
    ) -> Currency:
        values = data.model_dump(exclude_unset=True)
        return self.update(session, currency, values)
