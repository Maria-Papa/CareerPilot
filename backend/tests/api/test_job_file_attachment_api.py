from datetime import datetime, timezone
from typing import Callable

import pytest
from app.models.company import Company
from app.models.file import File
from app.models.job import Job
from app.models.job_file_attachment import JobFileAttachment
from app.models.user import User
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.utils.api_assertions import assert_404, assert_list, assert_status

pytestmark = pytest.mark.integration


def test_create_and_get_job_file_attachment(
    client: TestClient,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    job_factory: Callable[..., Job],
    file_factory: Callable[..., File],
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    file = file_factory(user_id=user.id)

    payload = {
        "file_id": file.id,
        "version": 1,
        "attached_at": datetime.now(timezone.utc).isoformat(),
    }

    resp = client.post(f"/api/v1/jobs/{job.id}/file-attachments", json=payload)
    assert_status(resp, 201)

    attachment_id = resp.json()["id"]

    resp = client.get(f"/api/v1/jobs/{job.id}/file-attachments/{attachment_id}")
    assert_status(resp, 200)
    assert resp.json()["id"] == attachment_id


def test_list_job_file_attachments(
    client: TestClient,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    job_factory: Callable[..., Job],
    file_factory: Callable[..., File],
    job_file_attachment_factory: Callable[..., JobFileAttachment],
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    file = file_factory(user_id=user.id)

    job_file_attachment_factory(job_id=job.id, file_id=file.id)
    job_file_attachment_factory(job_id=job.id, file_id=file.id)

    resp = client.get(f"/api/v1/jobs/{job.id}/file-attachments")
    assert_status(resp, 200)
    assert_list(resp)


def test_update_job_file_attachment(
    client: TestClient,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    job_factory: Callable[..., Job],
    file_factory: Callable[..., File],
    job_file_attachment_factory: Callable[..., JobFileAttachment],
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    file = file_factory(user_id=user.id)

    attachment = job_file_attachment_factory(job_id=job.id, file_id=file.id, version=1)

    resp = client.patch(
        f"/api/v1/jobs/{job.id}/file-attachments/{attachment.id}",
        json={"version": 2},
    )
    assert_status(resp, 200)
    assert resp.json()["version"] == 2


def test_delete_job_file_attachment(
    client: TestClient,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    job_factory: Callable[..., Job],
    file_factory: Callable[..., File],
    job_file_attachment_factory: Callable[..., JobFileAttachment],
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    file = file_factory(user_id=user.id)

    attachment = job_file_attachment_factory(job_id=job.id, file_id=file.id)

    resp = client.delete(
        f"/api/v1/jobs/{job.id}/file-attachments/{attachment.id}",
    )
    assert_status(resp, 204)

    resp = client.get(f"/api/v1/jobs/{job.id}/file-attachments/{attachment.id}")
    assert_404(resp)


def test_detach_job_file_attachment(
    client: TestClient,
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
    job_factory: Callable[..., Job],
    file_factory: Callable[..., File],
    job_file_attachment_factory: Callable[..., JobFileAttachment],
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    file = file_factory(user_id=user.id)

    attachment = job_file_attachment_factory(job_id=job.id, file_id=file.id)

    resp = client.post(
        f"/api/v1/jobs/{job.id}/file-attachments/{attachment.id}/detach",
    )
    assert_status(resp, 200)
    body = resp.json()
    assert body["is_active"] is False
    assert body["detached_at"] is not None
