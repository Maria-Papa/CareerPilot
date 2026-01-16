from unittest.mock import MagicMock

import pytest
from app.core.errors import ConflictError, EntityNotFoundError
from app.models.currency import Currency
from app.repositories.currency import CurrencyRepository
from app.schemas.currency import CurrencyCreate, CurrencyUpdate
from app.services.currency import CurrencyService

pytestmark = pytest.mark.unit


@pytest.fixture
def repo_mock() -> MagicMock:
    """Mocked CurrencyRepository with spec enforcement."""
    return MagicMock(spec=CurrencyRepository)


@pytest.fixture
def service(repo_mock: MagicMock) -> CurrencyService:
    """CurrencyService instance using the mocked repository."""
    return CurrencyService(repository=repo_mock)


def test_list_currencies(service: CurrencyService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    repo_mock.get_all.return_value = [
        Currency(id=1, code="AAA", symbol="A"),
        Currency(id=2, code="BBB", symbol="B"),
    ]

    result = service.list_currencies(session)

    repo_mock.get_all.assert_called_once()
    assert len(result) == 2


def test_get_currency_success(service: CurrencyService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    cur = Currency(id=1, code="GBP", symbol="£")
    repo_mock.get.return_value = cur

    result = service.get_currency(session, 1)

    assert result is cur


def test_get_currency_not_found(service: CurrencyService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    repo_mock.get.return_value = None

    with pytest.raises(EntityNotFoundError):
        service.get_currency(session, 999)


def test_create_currency(service: CurrencyService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    data = CurrencyCreate(code="EUR", symbol="€")
    created = Currency(id=10, code="EUR", symbol="€")

    repo_mock.find_one.return_value = None
    repo_mock.add.return_value = created

    result = service.create_currency(session, data)

    repo_mock.find_one.assert_called_once_with(session, code="EUR")
    repo_mock.add.assert_called_once()
    assert result.id == 10


def test_create_currency_conflict(
    service: CurrencyService, repo_mock: MagicMock
) -> None:
    session = MagicMock()
    data = CurrencyCreate(code="EUR", symbol="€")

    repo_mock.find_one.return_value = Currency(id=1, code="EUR", symbol="€")

    with pytest.raises(ConflictError):
        service.create_currency(session, data)


def test_update_currency(service: CurrencyService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    cur = Currency(id=1, code="AUD", symbol="$")
    data = CurrencyUpdate(code="ISD", symbol="€€")

    repo_mock.update.return_value = Currency(id=1, code="AUD", symbol="€€")

    result = service.update_currency(session, cur, data)

    repo_mock.update.assert_called_once()
    assert result.symbol == "€€"
