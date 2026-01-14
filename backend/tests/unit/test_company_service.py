# backend/tests/services/test_company_service.py
from unittest.mock import MagicMock

import pytest
from app.models import Company
from app.repositories.company import CompanyRepository
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.services.company import CompanyService

pytestmark = pytest.mark.unit


@pytest.fixture
def repo_mock():
    repo = MagicMock(spec=CompanyRepository)
    return repo


@pytest.fixture
def service(repo_mock):
    return CompanyService(repository=repo_mock)


def test_list_companies_calls_get_all(service, repo_mock):
    session = MagicMock()
    repo_mock.get_all.return_value = [Company(name="S1"), Company(name="S2")]
    result = service.list_companies(session, offset=0, limit=10)
    repo_mock.get_all.assert_called_once_with(session, offset=0, limit=10)
    assert len(result) == 2


def test_get_company_success(service, repo_mock):
    session = MagicMock()
    company = Company(id=1, name="Exists")
    repo_mock.get.return_value = company
    result = service.get_company(session, 1)
    assert result is company


def test_get_company_not_found_raises(service, repo_mock):
    session = MagicMock()
    repo_mock.get.return_value = None
    assert service.get_company(session, 999) is None


def test_get_company_including_deleted_success(service, repo_mock):
    session = MagicMock()
    company = Company(id=2, name="Deleted")
    repo_mock.get_including_deleted.return_value = company
    result = service.get_company_including_deleted(session, 2)
    assert result is company


def test_create_company(service, repo_mock):
    session = MagicMock()
    data = CompanyCreate.model_validate({"name": "CreateCo"})
    created = Company(id=10, name="CreateCo")
    repo_mock.add.return_value = created
    result = service.create_company(session, data)
    repo_mock.add.assert_called_once()
    assert result.id == 10


def test_update_company(service, repo_mock):
    session = MagicMock()
    company = Company(id=3, name="Old")
    data = CompanyUpdate.model_validate({"name": "NewName"})
    repo_mock.update.return_value = Company(id=3, name="NewName")
    result = service.update_company(session, company, data)
    repo_mock.update.assert_called_once()
    assert result.name == "NewName"


def test_delete_uses_soft_delete_for_soft_repo(service, repo_mock):
    session = MagicMock()
    company = Company(id=4, name="ToDelete")

    # If repository exposes soft_delete, service.delete should call it
    repo_mock.soft_delete = MagicMock()
    service.delete(session, company)
    repo_mock.soft_delete.assert_called_once_with(session, company)


def test_restore_calls_repository_restore(service, repo_mock):
    session = MagicMock()
    company = Company(id=5, name="ToRestore")
    repo_mock.restore = MagicMock()
    service.restore(session, company)
    repo_mock.restore.assert_called_once_with(session, company)
