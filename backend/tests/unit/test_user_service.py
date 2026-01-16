from unittest.mock import MagicMock

import pytest
from app.core.errors import ConflictError, EntityNotFoundError
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.user import UserService

pytestmark = pytest.mark.unit


@pytest.fixture
def repo_mock() -> MagicMock:
    return MagicMock(spec=UserRepository)


@pytest.fixture
def service(repo_mock: MagicMock) -> UserService:
    return UserService(repository=repo_mock)


def test_list_users(service: UserService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    repo_mock.get_all.return_value = [
        User(
            id=1, email="a@b.com", password_hash="x", is_active=True, is_verified=False
        ),
        User(
            id=2, email="c@d.com", password_hash="y", is_active=True, is_verified=True
        ),
    ]

    result = service.list(session)

    repo_mock.get_all.assert_called_once()
    assert len(result) == 2


def test_get_user_success(service: UserService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    user = User(
        id=1, email="a@b.com", password_hash="x", is_active=True, is_verified=False
    )
    repo_mock.get.return_value = user

    result = service.get_user(session, 1)

    assert result is user


def test_get_user_not_found(service: UserService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    repo_mock.get.return_value = None

    with pytest.raises(EntityNotFoundError):
        service.get_user(session, 999)


def test_create_user(service: UserService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    data = UserCreate(
        email="a@b.com", password="pwd", is_active=True, is_verified=False
    )
    created = User(
        id=10, email="a@b.com", password_hash="pwd", is_active=True, is_verified=False
    )

    repo_mock.find_one.return_value = None
    repo_mock.add.return_value = created

    result = service.create_user(session, data)

    repo_mock.find_one.assert_called_once_with(session, email="a@b.com")
    repo_mock.add.assert_called_once()
    assert result.id == 10


def test_create_user_conflict(service: UserService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    data = UserCreate(
        email="a@b.com", password="pwd", is_active=True, is_verified=False
    )

    repo_mock.find_one.return_value = User(
        id=1, email="a@b.com", password_hash="pwd", is_active=True, is_verified=False
    )

    with pytest.raises(ConflictError):
        service.create_user(session, data)


def test_update_user(service: UserService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    user = User(
        id=1, email="a@b.com", password_hash="x", is_active=True, is_verified=False
    )
    data = UserUpdate(is_verified=True)

    repo_mock.update.return_value = User(
        id=1, email="a@b.com", password_hash="x", is_active=True, is_verified=True
    )

    result = service.update_user(session, user, data)

    repo_mock.update.assert_called_once()
    assert result.is_verified is True
