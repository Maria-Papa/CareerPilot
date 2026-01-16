from unittest.mock import MagicMock

import pytest
from app.models.cost_of_living import CostOfLiving
from app.repositories.cost_of_living import CostOfLivingRepository
from app.schemas.cost_of_living import CostOfLivingCreate, CostOfLivingUpdate
from app.services.cost_of_living import CostOfLivingService

pytestmark = pytest.mark.unit


@pytest.fixture
def repo_mock() -> MagicMock:
    """Mocked CostOfLivingRepository with spec enforcement."""
    return MagicMock(spec=CostOfLivingRepository)


@pytest.fixture
def service(repo_mock: MagicMock) -> CostOfLivingService:
    """CostOfLivingService instance using the mocked repository."""
    return CostOfLivingService(repository=repo_mock)


def test_list_costs(service: CostOfLivingService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    repo_mock.get_all.return_value = [CostOfLiving(id=1), CostOfLiving(id=2)]

    result = service.list_costs(session)

    repo_mock.get_all.assert_called_once()
    assert len(result) == 2


def test_get_cost_success(service: CostOfLivingService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    col = CostOfLiving(id=1)
    repo_mock.get.return_value = col

    result = service.get_cost(session, 1)

    assert result is col


def test_get_cost_not_found(service: CostOfLivingService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    repo_mock.get.return_value = None

    with pytest.raises(Exception):
        service.get_cost(session, 999)


def test_create_cost(service: CostOfLivingService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    data = CostOfLivingCreate(location_id=1, yearly_cost=100000, title="Test")
    created = CostOfLiving(id=10)
    repo_mock.add.return_value = created

    result = service.create_cost(session, data)

    repo_mock.add.assert_called_once()
    assert result.id == 10


def test_update_cost(service: CostOfLivingService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    col = CostOfLiving(id=1)
    data = CostOfLivingUpdate(yearly_cost=200000)
    repo_mock.update.return_value = CostOfLiving(id=1, yearly_cost=200000)

    result = service.update_cost(session, col, data)

    repo_mock.update.assert_called_once()
    assert result.yearly_cost == 200000
