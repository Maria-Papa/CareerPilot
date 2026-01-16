from unittest.mock import MagicMock

import pytest
from app.core.error_handlers import EntityNotFoundError
from app.models.tag import Tag
from app.repositories.tag import TagRepository
from app.schemas.tag import TagCreate, TagUpdate
from app.services.tag import TagService
from sqlalchemy.orm import Session

pytestmark = pytest.mark.unit


@pytest.fixture
def repo_mock() -> MagicMock:
    """Mocked TagRepository with spec enforcement."""
    return MagicMock(spec=TagRepository)


@pytest.fixture
def service(repo_mock: MagicMock) -> TagService:
    """TagService instance using the mocked repository."""
    return TagService(repository=repo_mock)


def test_list_tags(service: TagService, repo_mock: MagicMock) -> None:
    session = MagicMock(spec=Session)
    repo_mock.get_all.return_value = [Tag(id=1, name="t1")]

    result = service.list_tags(session)

    repo_mock.get_all.assert_called_once()
    assert len(result) == 1
    assert result[0].name == "t1"


def test_get_tag_success(service: TagService, repo_mock: MagicMock) -> None:
    session = MagicMock(spec=Session)
    tag = Tag(id=1, name="t1")
    repo_mock.get.return_value = tag

    result = service.get_tag(session, 1)

    assert result is tag
    repo_mock.get.assert_called_once_with(session, 1)


def test_get_tag_not_found(service: TagService, repo_mock: MagicMock) -> None:
    session = MagicMock(spec=Session)
    repo_mock.get.return_value = None

    with pytest.raises(EntityNotFoundError):
        service.get_tag(session, 999)

    repo_mock.get.assert_called_once_with(session, 999)


def test_create_tag(service: TagService, repo_mock: MagicMock) -> None:
    session = MagicMock(spec=Session)
    data = TagCreate(name="new")
    created = Tag(id=10, name="new")
    repo_mock.add.return_value = created

    result = service.create_tag(session, data)

    repo_mock.add.assert_called_once()
    assert result.id == 10
    assert result.name == "new"


def test_update_tag(service: TagService, repo_mock: MagicMock) -> None:
    session = MagicMock(spec=Session)
    tag = Tag(id=1, name="old")
    data = TagUpdate(name="new")
    updated = Tag(id=1, name="new")
    repo_mock.update.return_value = updated

    result = service.update_tag(session, tag, data)

    repo_mock.update.assert_called_once()
    assert result.name == "new"


def test_delete_tag(service: TagService, repo_mock: MagicMock) -> None:
    session = MagicMock(spec=Session)
    tag = Tag(id=1, name="t1")

    service.delete_tag(session, tag)

    repo_mock.delete.assert_called_once_with(session, tag)
