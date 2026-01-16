from unittest.mock import MagicMock

import pytest
from app.core.error_handlers import EntityNotFoundError
from app.enums.job_event_type import JobEventType
from app.models.job_event import JobEvent
from app.repositories.job import JobRepository
from app.repositories.job_event import JobEventRepository
from app.schemas.job_event import JobEventCreate, JobEventUpdate
from app.services.job_event import JobEventService

pytestmark = pytest.mark.unit


@pytest.fixture
def repo_mock() -> MagicMock:
    return MagicMock(spec=JobEventRepository)


@pytest.fixture
def job_repo_mock() -> MagicMock:
    return MagicMock(spec=JobRepository)


@pytest.fixture
def service(repo_mock: MagicMock, job_repo_mock: MagicMock) -> JobEventService:
    return JobEventService(repository=repo_mock, job_repo=job_repo_mock)


def test_create_job_event_success(
    service: JobEventService, repo_mock: MagicMock, job_repo_mock: MagicMock
) -> None:
    session = MagicMock()
    job_repo_mock.get.return_value = object()
    data = JobEventCreate(
        event_type=JobEventType.APPLICATION_SUBMITTED,
        payload={"x": 1},
    )

    event = JobEvent(
        id=1,
        job_id=1,
        event_type=JobEventType.APPLICATION_SUBMITTED,
        payload={"x": 1},
    )
    repo_mock.add.return_value = event

    result = service.create_for_job(session, 1, data)
    assert result is event


def test_create_job_event_job_not_found(
    service: JobEventService, job_repo_mock: MagicMock
) -> None:
    session = MagicMock()
    job_repo_mock.get.return_value = None

    data = JobEventCreate(
        event_type=JobEventType.APPLICATION_SUBMITTED,
        payload=None,
    )

    with pytest.raises(EntityNotFoundError):
        service.create_for_job(session, 999, data)


def test_update_job_event_valid(
    service: JobEventService, repo_mock: MagicMock, job_repo_mock: MagicMock
) -> None:
    session = MagicMock()
    event = JobEvent(
        id=1,
        job_id=1,
        event_type=JobEventType.APPLICATION_SUBMITTED,
    )

    job_repo_mock.get.return_value = object()

    data = JobEventUpdate(payload={"updated": True})

    updated = JobEvent(
        id=1,
        job_id=1,
        event_type=JobEventType.APPLICATION_SUBMITTED,
        payload={"updated": True},
    )
    repo_mock.update.return_value = updated

    result = service.update_for_job(session, event, 1, data)
    assert result.payload == {"updated": True}


def test_get_job_event_success(service: JobEventService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    event = JobEvent(
        id=1,
        job_id=1,
        event_type=JobEventType.APPLICATION_SUBMITTED,
    )
    repo_mock.get.return_value = event

    result = service.get_job_event(session, 1)
    assert result is event


def test_get_job_event_not_found(
    service: JobEventService, repo_mock: MagicMock
) -> None:
    session = MagicMock()
    repo_mock.get.return_value = None

    with pytest.raises(EntityNotFoundError):
        service.get_job_event(session, 999)


def test_list_job_events_for_job(
    service: JobEventService, repo_mock: MagicMock
) -> None:
    session = MagicMock()
    repo_mock.find.return_value = [
        JobEvent(
            id=1,
            job_id=1,
            event_type=JobEventType.APPLICATION_SUBMITTED,
        )
    ]

    result = service.list_for_job(session, 1)
    assert len(result) == 1
    repo_mock.find.assert_called_once_with(session, job_id=1)


def test_delete_job_event(service: JobEventService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    event = JobEvent(
        id=1,
        job_id=1,
        event_type=JobEventType.APPLICATION_SUBMITTED,
    )

    service.delete(session, event)
    repo_mock.delete.assert_called_once_with(session, event)
