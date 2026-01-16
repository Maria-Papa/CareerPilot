import pytest
from app.models.currency import Currency
from app.repositories.currency import CurrencyRepository
from sqlalchemy.orm import Session

pytestmark = pytest.mark.repository


@pytest.fixture
def repo() -> CurrencyRepository:
    return CurrencyRepository()


def test_add_and_get(repo: CurrencyRepository, db_session: Session) -> None:
    cur = Currency(code="EUR", symbol="€")
    added = repo.add(db_session, cur)
    assert added.id is not None

    fetched = repo.get(db_session, added.id)
    assert fetched is not None
    assert fetched.code == "EUR"


def test_get_all(repo: CurrencyRepository, db_session: Session) -> None:
    repo.add(db_session, Currency(code="EUR", symbol="€"))
    repo.add(db_session, Currency(code="USD", symbol="$"))

    all_items = repo.get_all(db_session)
    assert len(all_items) >= 2


def test_update(repo: CurrencyRepository, db_session: Session) -> None:
    cur = Currency(code="EUR", symbol="€")
    repo.add(db_session, cur)

    updated = repo.update(db_session, cur, {"symbol": "€€"})
    assert updated.symbol == "€€"


def test_delete(repo: CurrencyRepository, db_session: Session) -> None:
    cur = Currency(code="EUR", symbol="€")
    repo.add(db_session, cur)

    repo.delete(db_session, cur)
    assert repo.get(db_session, cur.id) is None
