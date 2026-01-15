import pytest
from app.models import Company
from app.repositories.company import CompanyRepository
from sqlalchemy.orm import Session

pytestmark = pytest.mark.repository


@pytest.fixture
def repo() -> CompanyRepository:
    return CompanyRepository()


def test_add_and_get(repo, db_session: Session) -> None:
    company = Company(name="RepoCo", website="https://repo.co", industry="Repo")
    added = repo.add(db_session, company)
    assert added.id is not None

    fetched = repo.get(db_session, added.id)
    assert fetched is not None
    assert fetched.name == "RepoCo"


def test_get_all_and_find(repo, db_session: Session) -> None:
    c1 = Company(name="A", industry="X")
    c2 = Company(name="B", industry="Y")
    repo.add(db_session, c1)
    repo.add(db_session, c2)

    all_companies = repo.get_all(db_session)
    assert any(c.name == "A" for c in all_companies)
    assert any(c.name == "B" for c in all_companies)

    found = repo.find(db_session, industry="X")
    assert any(c.name == "A" for c in found)


def test_update(repo, db_session: Session) -> None:
    c = Company(name="ToUpdate", industry="Old")
    repo.add(db_session, c)
    updated = repo.update(db_session, c, {"industry": "New", "name": "UpdatedName"})
    assert updated.industry == "New"
    assert updated.name == "UpdatedName"


def test_soft_delete_and_restore(repo, db_session: Session) -> None:
    c = Company(name="SoftDeleteCo")
    repo.add(db_session, c)
    repo.soft_delete(db_session, c)

    # After soft delete, default get should return None
    assert repo.get(db_session, c.id) is None

    # get_including_deleted should return the instance
    inc = repo.get_including_deleted(db_session, c.id)
    assert inc is not None
    assert inc.id == c.id

    # restore and verify get returns it again
    repo.restore(db_session, inc)
    assert repo.get(db_session, c.id) is not None


def test_delete_permanent(repo, db_session: Session) -> None:
    # BaseRepository.delete should remove permanently
    c = Company(name="PermanentDelete")
    repo.add(db_session, c)
    repo.delete(db_session, c)
    assert repo.get_including_deleted(db_session, c.id) is None
