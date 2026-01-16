from unittest.mock import MagicMock

import pytest
from app.enums.file_type import FileType
from app.models.file import File
from app.repositories.file import FileRepository
from app.schemas.file import FileCreate, FileUpdate
from app.services.file import FileService

pytestmark = pytest.mark.unit


@pytest.fixture
def repo_mock() -> MagicMock:
    """Mocked FileRepository with spec enforcement."""
    return MagicMock(spec=FileRepository)


@pytest.fixture
def service(repo_mock: MagicMock) -> FileService:
    """FileService instance using the mocked repository."""
    return FileService(repository=repo_mock)


def test_list(service: FileService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    repo_mock.get_all.return_value = [
        File(id=1, user_id=1, file_url="a", file_type=FileType.CV),
        File(id=2, user_id=1, file_url="b", file_type=FileType.CV),
    ]

    result = service.list(session)
    repo_mock.get_all.assert_called_once()
    assert len(result) == 2


def test_get_success(service: FileService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    file = File(id=1, user_id=1, file_url="x", file_type=FileType.CV)
    repo_mock.get.return_value = file

    result = service.get(session, 1)
    assert result is file


def test_get_not_found(service: FileService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    repo_mock.get.return_value = None

    result = service.get(session, 999)
    assert result is None


def test_create_file(service: FileService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    data = FileCreate(user_id=1, file_url="http://x", file_type=FileType.CV)
    created = File(id=10, user_id=1, file_url="http://x", file_type=FileType.CV)

    repo_mock.add.return_value = created

    result = service.create_file(session, data)
    repo_mock.add.assert_called_once()
    assert result.id == 10


def test_update_file(service: FileService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    file = File(id=1, user_id=1, file_url="old", file_type=FileType.CV)
    data = FileUpdate(file_url="new")

    repo_mock.update.return_value = File(
        id=1, user_id=1, file_url="new", file_type=FileType.CV
    )

    result = service.update_file(session, file, data)
    repo_mock.update.assert_called_once()
    assert result.file_url == "new"


def test_restore(service: FileService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    file = File(id=1, user_id=1, file_url="x", file_type=FileType.CV)

    service.restore(session, file)
    repo_mock.restore.assert_called_once()
