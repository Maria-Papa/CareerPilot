import pytest
from app.models import Location
from app.repositories.location import LocationRepository
from sqlalchemy.orm import Session

pytestmark = pytest.mark.repository


@pytest.fixture
def repo() -> LocationRepository:
    return LocationRepository()


def test_add_and_get(repo: LocationRepository, db_session: Session) -> None:
    loc = Location(name="Athens", country_code="GR", currency_id=1)
    added = repo.add(db_session, loc)
    assert added.id is not None

    fetched = repo.get(db_session, added.id)
    assert fetched is not None
    assert fetched.name == "Athens"


def test_get_all(repo: LocationRepository, db_session: Session) -> None:
    repo.add(db_session, Location(name="A", country_code="GR", currency_id=1))
    repo.add(db_session, Location(name="B", country_code="SE", currency_id=1))

    all_items = repo.get_all(db_session)
    assert len(all_items) >= 2


def test_update(repo: LocationRepository, db_session: Session) -> None:
    loc = Location(name="Old", country_code="GR", currency_id=1)
    repo.add(db_session, loc)

    updated = repo.update(db_session, loc, {"name": "New"})
    assert updated.name == "New"


def test_delete(repo: LocationRepository, db_session: Session) -> None:
    loc = Location(name="ToDelete", country_code="GR", currency_id=1)
    repo.add(db_session, loc)

    repo.delete(db_session, loc)
    assert repo.get(db_session, loc.id) is None
