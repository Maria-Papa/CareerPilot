from app.models import Currency
from sqlalchemy.orm import Session


def create_currency(db_session: Session, **kwargs) -> Currency:
    defaults = {
        "code": "EUR",
        "symbol": "€",
    }
    defaults.update(kwargs)

    currency = Currency(**defaults)
    db_session.add(currency)
    db_session.commit()
    db_session.refresh(currency)
    return currency
