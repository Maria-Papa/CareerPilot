import pytest
from app.repositories.job_tag import JobTagRepository
from sqlalchemy.orm import Session
from tests.factories.company import create_company
from tests.factories.job import create_job
from tests.factories.job_tag import create_job_tag
from tests.factories.tag import create_tag
from tests.factories.user import create_user

pytestmark = pytest.mark.repository


@pytest.fixture
def repo() -> JobTagRepository:
    return JobTagRepository()


def test_add_and_get_job_tag(repo: JobTagRepository, db_session: Session):
    user = create_user(db_session)
    company = create_company(db_session)
    job = create_job(db_session, user_id=user.id, company_id=company.id)
    tag = create_tag(db_session)

    link = create_job_tag(db_session, job_id=job.id, tag_id=tag.id)

    fetched = repo.find_one(db_session, job_id=job.id, tag_id=tag.id)
    assert fetched is not None
    assert fetched.job_id == job.id
    assert fetched.tag_id == tag.id


def test_get_all_and_find_job_tag(repo: JobTagRepository, db_session: Session):
    user = create_user(db_session)
    company = create_company(db_session)
    job = create_job(db_session, user_id=user.id, company_id=company.id)
    tag1 = create_tag(db_session)
    tag2 = create_tag(db_session)

    create_job_tag(db_session, job_id=job.id, tag_id=tag1.id)
    create_job_tag(db_session, job_id=job.id, tag_id=tag2.id)

    all_links = repo.get_all(db_session)
    assert len(all_links) >= 2

    found = repo.find(db_session, job_id=job.id)
    assert len(found) == 2


def test_delete_job_tag(repo: JobTagRepository, db_session: Session):
    user = create_user(db_session)
    company = create_company(db_session)
    job = create_job(db_session, user_id=user.id, company_id=company.id)
    tag = create_tag(db_session)

    link = create_job_tag(db_session, job_id=job.id, tag_id=tag.id)

    repo.delete(db_session, link)
    assert repo.find_one(db_session, job_id=job.id, tag_id=tag.id) is None
