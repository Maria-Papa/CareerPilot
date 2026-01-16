import pytest
from app.models.user import User
from app.repositories.user import UserRepository
from sqlalchemy.orm import Session

pytestmark = pytest.mark.repository


@pytest.fixture
def repo() -> UserRepository:
    return UserRepository()


def test_add_and_get(repo: UserRepository, db_session: Session) -> None:
    user = User(email="a@b.com", password_hash="x", is_active=True, is_verified=False)
    added = repo.add(db_session, user)

    fetched = repo.get(db_session, added.id)
    assert fetched is not None
    assert fetched.email == "a@b.com"


def test_get_all(repo: UserRepository, db_session: Session) -> None:
    repo.add(
        db_session,
        User(email="a@b.com", password_hash="x", is_active=True, is_verified=False),
    )
    repo.add(
        db_session,
        User(email="c@d.com", password_hash="y", is_active=True, is_verified=False),
    )

    results = repo.get_all(db_session)
    assert len(results) >= 2


def test_update(repo: UserRepository, db_session: Session) -> None:
    user = User(email="a@b.com", password_hash="x", is_active=True, is_verified=False)
    repo.add(db_session, user)

    updated = repo.update(db_session, user, {"is_verified": True})
    assert updated.is_verified is True


def test_soft_delete_and_restore(repo: UserRepository, db_session: Session) -> None:
    user = User(email="a@b.com", password_hash="x", is_active=True, is_verified=False)
    repo.add(db_session, user)

    repo.soft_delete(db_session, user)
    assert repo.get(db_session, user.id) is None

    repo.restore(db_session, user)
    assert repo.get(db_session, user.id) is not None
