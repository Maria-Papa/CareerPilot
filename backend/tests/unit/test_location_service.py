from unittest.mock import MagicMock

import pytest
from app.models.location import Location
from app.repositories.location import LocationRepository
from app.schemas.location import LocationCreate, LocationUpdate
from app.services.location import LocationService

pytestmark = pytest.mark.unit


@pytest.fixture
def repo_mock() -> MagicMock:
    """Mocked LocationRepository with spec enforcement."""
    return MagicMock(spec=LocationRepository)


@pytest.fixture
def service(repo_mock: MagicMock) -> LocationService:
    """LocationService instance using the mocked repository."""
    return LocationService(repository=repo_mock)


def test_list_locations(service: LocationService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    repo_mock.get_all.return_value = [Location(id=1), Location(id=2)]

    result = service.list_locations(session)

    repo_mock.get_all.assert_called_once()
    assert len(result) == 2


def test_get_location_success(service: LocationService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    loc = Location(id=1)
    repo_mock.get.return_value = loc

    result = service.get(session, 1)

    assert result is loc


def test_get_location_not_found(service: LocationService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    repo_mock.get.return_value = None

    result = service.get(session, 999)

    assert result is None


def test_create_location(service: LocationService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    data = LocationCreate(name="Athens", country_code="GR", currency_id=1)
    created = Location(id=10)
    repo_mock.add.return_value = created

    result = service.create_location(session, data)

    repo_mock.add.assert_called_once()
    assert result.id == 10


def test_update_location(service: LocationService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    loc = Location(id=1)
    data = LocationUpdate(name="NewName")
    repo_mock.update.return_value = Location(id=1, name="NewName")

    result = service.update_location(session, loc, data)

    repo_mock.update.assert_called_once()
    assert result.name == "NewName"


def test_delete_location(service: LocationService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    loc = Location(id=1)

    service.delete(session, loc)

    repo_mock.delete.assert_called_once_with(session, loc)
