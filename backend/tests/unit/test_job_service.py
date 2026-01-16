from unittest.mock import MagicMock

import pytest
from app.core.errors import EntityNotFoundError, InvalidStateTransitionError
from app.enums.job_status import JobStatus
from app.models.job import Job
from app.models.job_file_attachment import JobFileAttachment
from app.models.job_status_history import JobStatusHistory
from app.repositories.company import CompanyRepository
from app.repositories.job import JobRepository
from app.repositories.location import LocationRepository
from app.repositories.user import UserRepository
from app.schemas.job import JobCreate, JobUpdate
from app.services.job import JobService
from requests import session

pytestmark = pytest.mark.unit


@pytest.fixture
def repo_mock() -> MagicMock:
    return MagicMock(spec=JobRepository)


@pytest.fixture
def user_repo_mock() -> MagicMock:
    return MagicMock(spec=UserRepository)


@pytest.fixture
def company_repo_mock() -> MagicMock:
    return MagicMock(spec=CompanyRepository)


@pytest.fixture
def location_repo_mock() -> MagicMock:
    return MagicMock(spec=LocationRepository)


@pytest.fixture
def service(
    repo_mock: MagicMock,
    user_repo_mock: MagicMock,
    company_repo_mock: MagicMock,
    location_repo_mock: MagicMock,
) -> JobService:
    return JobService(
        repository=repo_mock,
        user_repo=user_repo_mock,
        company_repo=company_repo_mock,
        location_repo=location_repo_mock,
    )


def test_create_job_success(
    service: JobService,
    repo_mock: MagicMock,
    user_repo_mock: MagicMock,
    company_repo_mock: MagicMock,
    location_repo_mock: MagicMock,
) -> None:
    session = MagicMock()
    user_repo_mock.get.return_value = True
    company_repo_mock.get.return_value = True
    location_repo_mock.get.return_value = True

    data = JobCreate(
        user_id=1,
        company_id=1,
        location_id=1,
        title="Test",
        current_status=JobStatus.APPLIED,
    )

    job = Job(
        id=1, user_id=1, company_id=1, title="Test", current_status=JobStatus.APPLIED
    )
    repo_mock.add.return_value = job

    result = service.create_job(session, data, user_id=1)
    assert result is job


def test_create_job_user_not_found(
    service: JobService, user_repo_mock: MagicMock
) -> None:
    session = MagicMock()
    user_repo_mock.get.return_value = None

    data = JobCreate(
        user_id=999,
        company_id=1,
        location_id=1,
        title="Test",
        current_status=JobStatus.APPLIED,
    )

    with pytest.raises(EntityNotFoundError):
        service.create_job(session, data, user_id=999)


def test_update_job(
    service: JobService,
    repo_mock: MagicMock,
    user_repo_mock: MagicMock,
    company_repo_mock: MagicMock,
    location_repo_mock: MagicMock,
) -> None:
    session = MagicMock()
    job = Job(
        id=1, user_id=1, company_id=1, title="Old", current_status=JobStatus.APPLIED
    )

    user_repo_mock.get.return_value = True
    company_repo_mock.get.return_value = True
    location_repo_mock.get.return_value = True

    data = JobUpdate(title="New")
    updated = Job(
        id=1, user_id=1, company_id=1, title="New", current_status=JobStatus.APPLIED
    )
    repo_mock.update.return_value = updated

    result = service.update_job(session, job, data)
    assert result.title == "New"


def test_change_status_success(service: JobService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    job = Job(id=1, current_status=JobStatus.APPLIED)

    result = service.change_status(session, job, JobStatus.INTERVIEW)
    assert result.current_status == JobStatus.INTERVIEW


def test_change_status_rejected(service: JobService, repo_mock: MagicMock) -> None:
    session = MagicMock()
    job = Job(id=1, current_status=JobStatus.REJECTED)

    with pytest.raises(InvalidStateTransitionError):
        service.change_status(session, job, JobStatus.INTERVIEW)


def test_attach_file(service: JobService, repo_mock: MagicMock):
    session = MagicMock()
    job = Job(id=1)

    attachment = JobFileAttachment(id=10, job_id=1, file_id=1, version=1)
    repo_mock.add_file_attachment.return_value = attachment

    result = service.attach_file(session, job, file_id=1, version=1)
    assert result is attachment
