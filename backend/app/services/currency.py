from sqlalchemy.orm import Session
from app.models import Currency
from app.repositories import CurrencyRepository
from app.services import BaseService
from app.schemas import CurrencyCreate, CurrencyUpdate


class CurrencyService(BaseService[Currency]):
    repository: CurrencyRepository

    def __init__(self):
        super().__init__(CurrencyRepository())

    def create_currency(self, session: Session, data: CurrencyCreate) -> Currency:
        currency = Currency(**data.model_dump())
        return self.create(session, currency)

    def update_currency(
        self, session: Session, currency: Currency, data: CurrencyUpdate
    ) -> Currency:
        values = data.model_dump(exclude_unset=True)
        return self.update(session, currency, values)
