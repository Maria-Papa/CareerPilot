import pytest
from app.models.cost_of_living import CostOfLiving
from app.repositories.cost_of_living import CostOfLivingRepository
from sqlalchemy.orm import Session

pytestmark = pytest.mark.repository


@pytest.fixture
def repo() -> CostOfLivingRepository:
    return CostOfLivingRepository()


def test_add_and_get(repo: CostOfLivingRepository, db_session: Session) -> None:
    col = CostOfLiving(location_id=1, yearly_cost=100000, title="Test")
    added = repo.add(db_session, col)
    assert added.id is not None

    fetched = repo.get(db_session, added.id)
    assert fetched is not None
    assert fetched.yearly_cost == 100000


def test_get_all(repo: CostOfLivingRepository, db_session: Session) -> None:
    repo.add(db_session, CostOfLiving(location_id=1, yearly_cost=100000))
    repo.add(db_session, CostOfLiving(location_id=2, yearly_cost=200000))

    all_items = repo.get_all(db_session)
    assert len(all_items) >= 2


def test_update(repo: CostOfLivingRepository, db_session: Session) -> None:
    col = CostOfLiving(location_id=1, yearly_cost=100000)
    repo.add(db_session, col)

    updated = repo.update(db_session, col, {"yearly_cost": 150000})
    assert updated.yearly_cost == 150000


def test_delete(repo: CostOfLivingRepository, db_session: Session) -> None:
    col = CostOfLiving(location_id=1, yearly_cost=100000)
    repo.add(db_session, col)

    repo.delete(db_session, col)
    assert repo.get(db_session, col.id) is None
