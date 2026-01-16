from datetime import datetime, timezone
from unittest.mock import ANY, MagicMock

import pytest
from app.models.job_file_attachment import JobFileAttachment
from app.repositories.job_file_attachment import JobFileAttachmentRepository
from app.schemas.job_file_attachment import (
    JobFileAttachmentCreate,
    JobFileAttachmentUpdate,
)
from app.services.job_file_attachment import JobFileAttachmentService

pytestmark = pytest.mark.unit


@pytest.fixture
def repo_mock() -> MagicMock:
    return MagicMock(spec=JobFileAttachmentRepository)


@pytest.fixture
def service(repo_mock: MagicMock) -> JobFileAttachmentService:
    svc = JobFileAttachmentService()
    svc.repository = repo_mock
    return svc


def test_create_attachment(
    service: JobFileAttachmentService, repo_mock: MagicMock
) -> None:
    session = MagicMock()
    data = JobFileAttachmentCreate(
        file_id=2,
        version=1,
        attached_at=datetime.now(timezone.utc),
    )

    created = JobFileAttachment(id=1, job_id=1, file_id=2, version=1)
    repo_mock.add.return_value = created

    result = service.create_attachment(session, 1, data)

    repo_mock.add.assert_called_once()
    assert result is created


def test_update_attachment(
    service: JobFileAttachmentService, repo_mock: MagicMock
) -> None:
    session = MagicMock()
    attachment = JobFileAttachment(id=1, job_id=1, file_id=2, version=1)

    data = JobFileAttachmentUpdate(version=2)
    updated = JobFileAttachment(id=1, job_id=1, file_id=2, version=2)
    repo_mock.update.return_value = updated

    result = service.update_attachment(session, attachment, data)

    repo_mock.update.assert_called_once_with(
        session,
        attachment,
        {"version": 2},
    )
    assert result is updated


def test_detach_attachment(
    service: JobFileAttachmentService, repo_mock: MagicMock
) -> None:
    session = MagicMock()
    attachment = JobFileAttachment(
        id=1,
        job_id=1,
        file_id=2,
        version=1,
        is_active=True,
        attached_at=datetime.now(timezone.utc),
        detached_at=None,
    )

    updated = JobFileAttachment(
        id=1,
        job_id=1,
        file_id=2,
        version=1,
        is_active=False,
        attached_at=attachment.attached_at,
        detached_at=datetime.now(timezone.utc),
    )
    repo_mock.update.return_value = updated

    result = service.detach_attachment(session, attachment)

    repo_mock.update.assert_called_once_with(
        session,
        attachment,
        {
            "detached_at": ANY,
            "is_active": False,
        },
    )
    assert result is updated
