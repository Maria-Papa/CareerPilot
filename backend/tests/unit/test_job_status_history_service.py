from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest
from app.core.errors import EntityNotFoundError
from app.enums.job_status import JobStatus
from app.models.job_status_history import JobStatusHistory
from app.repositories.job import JobRepository
from app.repositories.job_status_history import JobStatusHistoryRepository
from app.schemas.job_status_history import (
    JobStatusHistoryCreate,
    JobStatusHistoryUpdate,
)
from app.services.job_status_history import JobStatusHistoryService
from sqlalchemy.orm import Session

pytestmark = pytest.mark.unit


@pytest.fixture
def repo_mock() -> MagicMock:
    return MagicMock(spec=JobStatusHistoryRepository)


@pytest.fixture
def job_repo_mock() -> MagicMock:
    return MagicMock(spec=JobRepository)


@pytest.fixture
def service(repo_mock: MagicMock, job_repo_mock: MagicMock) -> JobStatusHistoryService:
    svc = JobStatusHistoryService()
    svc.repository = repo_mock
    svc._job_repo = job_repo_mock
    return svc


def test_create_history_valid_job(
    service: JobStatusHistoryService, repo_mock: MagicMock, job_repo_mock: MagicMock
):
    session = MagicMock(spec=Session)
    job_repo_mock.get.return_value = object()

    data = JobStatusHistoryCreate(status=JobStatus.APPLIED)
    history = JobStatusHistory(id=1, job_id=1, status=JobStatus.APPLIED)
    repo_mock.add.return_value = history

    result = service.create_history(session, 1, data)

    job_repo_mock.get.assert_called_once_with(session, 1)
    repo_mock.add.assert_called_once()
    assert result is history


def test_create_history_invalid_job_raises(
    service: JobStatusHistoryService, job_repo_mock: MagicMock
):
    session = MagicMock(spec=Session)
    job_repo_mock.get.return_value = None

    data = JobStatusHistoryCreate(status=JobStatus.APPLIED)

    with pytest.raises(EntityNotFoundError):
        service.create_history(session, 1, data)


def test_update_history(service: JobStatusHistoryService, repo_mock: MagicMock):
    session = MagicMock(spec=Session)
    history = JobStatusHistory(id=1, job_id=1, status=JobStatus.APPLIED)

    data = JobStatusHistoryUpdate(status=JobStatus.INTERVIEW)
    updated = JobStatusHistory(id=1, job_id=1, status=JobStatus.INTERVIEW)
    repo_mock.update.return_value = updated

    result = service.update_history(session, history, data)

    repo_mock.update.assert_called_once_with(
        session,
        history,
        {"status": JobStatus.INTERVIEW},
    )
    assert result is updated
