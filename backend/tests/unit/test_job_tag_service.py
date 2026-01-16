from unittest.mock import MagicMock

import pytest
from app.core.errors import EntityNotFoundError
from app.models.job_tag import JobTag
from app.repositories.job import JobRepository
from app.repositories.job_tag import JobTagRepository
from app.repositories.tag import TagRepository
from app.schemas.job_tag import JobTagCreate, JobTagUpdate
from app.services.job_tag import JobTagService
from sqlalchemy.orm import Session

pytestmark = pytest.mark.unit


@pytest.fixture
def repo_mock() -> MagicMock:
    return MagicMock(spec=JobTagRepository)


@pytest.fixture
def job_repo_mock() -> MagicMock:
    return MagicMock(spec=JobRepository)


@pytest.fixture
def tag_repo_mock() -> MagicMock:
    return MagicMock(spec=TagRepository)


@pytest.fixture
def service(
    repo_mock: MagicMock, job_repo_mock: MagicMock, tag_repo_mock: MagicMock
) -> JobTagService:
    svc = JobTagService()
    svc.repository = repo_mock
    svc._job_repo = job_repo_mock
    svc._tag_repo = tag_repo_mock
    return svc


def test_create_tag_valid(
    service: JobTagService,
    repo_mock: MagicMock,
    job_repo_mock: MagicMock,
    tag_repo_mock: MagicMock,
) -> None:
    session = MagicMock(spec=Session)
    job_repo_mock.get.return_value = object()
    tag_repo_mock.get.return_value = object()

    data = JobTagCreate(tag_id=5)
    link = JobTag(job_id=1, tag_id=5)
    repo_mock.add.return_value = link

    result = service.create_tag(session, 1, data)

    job_repo_mock.get.assert_called_once_with(session, 1)
    tag_repo_mock.get.assert_called_once_with(session, 5)
    repo_mock.add.assert_called_once()
    assert result is link


def test_create_tag_invalid_job(
    service: JobTagService, job_repo_mock: MagicMock
) -> None:
    session = MagicMock(spec=Session)
    job_repo_mock.get.return_value = None

    with pytest.raises(EntityNotFoundError):
        service.create_tag(session, 1, JobTagCreate(tag_id=5))


def test_create_tag_invalid_tag(
    service: JobTagService, job_repo_mock: MagicMock, tag_repo_mock: MagicMock
) -> None:
    session = MagicMock(spec=Session)
    job_repo_mock.get.return_value = object()
    tag_repo_mock.get.return_value = None

    with pytest.raises(EntityNotFoundError):
        service.create_tag(session, 1, JobTagCreate(tag_id=5))


def test_update_tag(service: JobTagService, repo_mock: MagicMock) -> None:
    session = MagicMock(spec=Session)
    link = JobTag(job_id=1, tag_id=2)

    data = JobTagUpdate(tag_id=3)
    updated = JobTag(job_id=1, tag_id=3)
    repo_mock.update.return_value = updated

    result = service.update_tag(session, link, data)

    repo_mock.update.assert_called_once_with(session, link, {"tag_id": 3})
    assert result is updated
