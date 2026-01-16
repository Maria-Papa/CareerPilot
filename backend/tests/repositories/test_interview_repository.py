from typing import Callable

import pytest
from app.models.company import Company
from app.models.interview import Interview
from app.models.job import Job
from app.models.user import User
from app.repositories.interview import InterviewRepository
from sqlalchemy.orm import Session

pytestmark = pytest.mark.repository


@pytest.fixture
def repo() -> InterviewRepository:
    return InterviewRepository()


def test_add_and_get(
    repo: InterviewRepository,
    db_session: Session,
    interview_factory: Callable[..., Interview],
    job_factory: Callable[..., Job],
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    interview = interview_factory(job_id=job.id)

    fetched = repo.get(db_session, interview.id)
    assert fetched is not None
    assert fetched.id == interview.id


def test_get_all(
    repo: InterviewRepository,
    db_session: Session,
    interview_factory: Callable[..., Interview],
    job_factory: Callable[..., Job],
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    interview_factory(job_id=job.id)
    interview_factory(job_id=job.id)

    results = repo.get_all(db_session)
    assert len(results) >= 2


def test_update(
    repo: InterviewRepository,
    db_session: Session,
    interview_factory: Callable[..., Interview],
    job_factory: Callable[..., Job],
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    interview = interview_factory(job_id=job.id, notes="Old")
    updated = repo.update(db_session, interview, {"notes": "New"})
    assert updated.notes == "New"


def test_delete(
    repo: InterviewRepository,
    db_session: Session,
    interview_factory: Callable[..., Interview],
    job_factory: Callable[..., Job],
    user_factory: Callable[..., User],
    company_factory: Callable[..., Company],
) -> None:
    user = user_factory()
    company = company_factory()
    job = job_factory(user_id=user.id, company_id=company.id)

    interview = interview_factory(job_id=job.id)
    repo.delete(db_session, interview)

    assert repo.get(db_session, interview.id) is None
