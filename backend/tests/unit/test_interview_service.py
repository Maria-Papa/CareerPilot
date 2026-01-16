from datetime import datetime
from unittest.mock import MagicMock

import pytest
from app.core.errors import EntityNotFoundError
from app.enums.interview_type import InterviewType
from app.models.interview import Interview
from app.repositories.interview import InterviewRepository
from app.repositories.job import JobRepository
from app.schemas.interview import InterviewCreate, InterviewUpdate
from app.services.interview import InterviewService

pytestmark = pytest.mark.unit


@pytest.fixture
def repo_mock() -> MagicMock:
    return MagicMock(spec=InterviewRepository)


@pytest.fixture
def job_repo_mock() -> MagicMock:
    return MagicMock(spec=JobRepository)


@pytest.fixture
def service(repo_mock: MagicMock, job_repo_mock: MagicMock) -> InterviewService:
    return InterviewService(repository=repo_mock, job_repo=job_repo_mock)


def test_create_interview_success(
    service: InterviewService, repo_mock: MagicMock, job_repo_mock: MagicMock
) -> None:
    session = MagicMock()
    job_repo_mock.get.return_value = object()

    data = InterviewCreate(
        interview_type=InterviewType.HR_SCREEN,
        scheduled_at=datetime.utcnow(),
        outcome=None,
        notes=None,
    )

    interview = Interview(id=1, job_id=1, interview_type=InterviewType.HR_SCREEN)
    repo_mock.add.return_value = interview

    result = service.create_interview(session, job_id=1, data=data)
    assert result is interview


def test_create_interview_job_not_found(
    service: InterviewService, job_repo_mock: MagicMock
) -> None:
    session = MagicMock()
    job_repo_mock.get.return_value = None

    data = InterviewCreate(
        interview_type=InterviewType.HR_SCREEN,
        scheduled_at=datetime.utcnow(),
        outcome=None,
        notes=None,
    )

    with pytest.raises(EntityNotFoundError):
        service.create_interview(session, job_id=999, data=data)


def test_update_interview_valid(
    service: InterviewService, repo_mock: MagicMock, job_repo_mock: MagicMock
) -> None:
    session = MagicMock()
    interview = Interview(id=1, job_id=1, interview_type=InterviewType.HR_SCREEN)

    data = InterviewUpdate(notes="Updated notes")
    updated = Interview(
        id=1, job_id=1, interview_type=InterviewType.HR_SCREEN, notes="Updated notes"
    )
    repo_mock.update.return_value = updated

    result = service.update_interview(session, interview, data)
    assert result.notes == "Updated notes"


def test_reschedule(service: InterviewService) -> None:
    session = MagicMock()
    interview = Interview(id=1, job_id=1, interview_type=InterviewType.HR_SCREEN)
    new_time = datetime.utcnow()

    result = service.reschedule(session, interview, new_time)
    assert result.scheduled_at == new_time
