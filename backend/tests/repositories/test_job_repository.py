from typing import Callable

import pytest
from app.enums.job_status import JobStatus
from app.models.company import Company
from app.models.job import Job
from app.models.job_file_attachment import JobFileAttachment
from app.models.job_status_history import JobStatusHistory
from app.models.user import User
from app.repositories.job import JobRepository
from sqlalchemy.orm import Session

pytestmark = pytest.mark.repository


@pytest.fixture
def repo() -> JobRepository:
    return JobRepository()


def test_add_and_get(
    repo: JobRepository,
    db_session: Session,
    job_factory: Callable[..., Job],
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
):
    user = user_factory()
    company = company_factory()

    job = job_factory(user_id=user.id, company_id=company.id)

    fetched = repo.get(db_session, job.id)
    assert fetched is not None
    assert fetched.id == job.id


def test_get_all(
    repo: JobRepository,
    db_session: Session,
    job_factory: Callable[..., Job],
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
):
    user = user_factory()
    company = company_factory()

    job_factory(user_id=user.id, company_id=company.id)
    job_factory(user_id=user.id, company_id=company.id)

    results = repo.get_all(db_session)
    assert len(results) >= 2


def test_update(
    repo: JobRepository,
    db_session: Session,
    job_factory: Callable[..., Job],
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
):
    user = user_factory()
    company = company_factory()

    job = job_factory(user_id=user.id, company_id=company.id, title="Old Title")
    updated = repo.update(db_session, job, {"title": "New Title"})
    assert updated.title == "New Title"


def test_soft_delete_and_restore(
    repo: JobRepository,
    db_session: Session,
    job_factory: Callable[..., Job],
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
):
    user = user_factory()
    company = company_factory()

    job = job_factory(user_id=user.id, company_id=company.id)

    repo.soft_delete(db_session, job)
    assert repo.get(db_session, job.id) is None

    repo.restore(db_session, job)
    restored = repo.get(db_session, job.id)
    assert restored is not None


def test_add_status_history(
    repo: JobRepository,
    db_session: Session,
    job_factory: Callable[..., Job],
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
):
    user = user_factory()
    company = company_factory()

    job = job_factory(user_id=user.id, company_id=company.id)

    history = JobStatusHistory(job_id=job.id, status=JobStatus.INTERVIEW)
    saved = repo.add_status_history(db_session, history)
    assert saved.id is not None


def test_add_file_attachment(
    repo: JobRepository,
    db_session: Session,
    job_factory: Callable[..., Job],
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
):
    user = user_factory()
    company = company_factory()

    job = job_factory(user_id=user.id, company_id=company.id)

    attachment = JobFileAttachment(
        job_id=job.id,
        file_id=1,
        version=1,
        is_active=True,
    )
    saved = repo.add_file_attachment(db_session, attachment)
    assert saved.id is not None
