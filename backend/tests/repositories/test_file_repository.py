from typing import Callable

import pytest
from app.models.file import File
from app.models.user import User
from app.repositories.file import FileRepository
from sqlalchemy.orm import Session

pytestmark = pytest.mark.repository


@pytest.fixture
def repo() -> FileRepository:
    return FileRepository()


def test_add_and_get(
    repo: FileRepository,
    db_session: Session,
    file_factory: Callable[..., File],
    user_factory: Callable[..., User],
) -> None:
    user = user_factory()
    file = file_factory(user_id=user.id)

    fetched = repo.get(db_session, file.id)
    assert fetched is not None
    assert fetched.id == file.id


def test_get_all(
    repo: FileRepository,
    db_session: Session,
    file_factory: Callable[..., File],
    user_factory: Callable[..., User],
) -> None:
    user = user_factory()
    file_factory(user_id=user.id)
    file_factory(user_id=user.id)

    results = repo.get_all(db_session)
    assert len(results) >= 2


def test_update(
    repo: FileRepository,
    db_session: Session,
    file_factory: Callable[..., File],
    user_factory: Callable[..., User],
) -> None:
    user = user_factory()
    file = file_factory(user_id=user.id)

    updated = repo.update(db_session, file, {"file_url": "http://updated.com"})
    assert updated.file_url == "http://updated.com"


def test_soft_delete_and_restore(
    repo: FileRepository,
    db_session: Session,
    file_factory: Callable[..., File],
    user_factory: Callable[..., User],
) -> None:
    user = user_factory()
    file = file_factory(user_id=user.id)

    repo.soft_delete(db_session, file)
    assert repo.get(db_session, file.id) is None

    repo.restore(db_session, file)
    restored = repo.get(db_session, file.id)
    assert restored is not None
