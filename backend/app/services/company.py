from typing import Sequence

from app.core import EntityNotFoundError
from app.models import Company
from app.repositories.company import CompanyRepository
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.services.soft_delete_base import SoftDeleteService
from sqlalchemy.orm import Session


class CompanyService(SoftDeleteService[Company]):
    def __init__(self, repository: CompanyRepository | None = None) -> None:
        repository = repository or CompanyRepository()
        super().__init__(repository)

    def list_companies(
        self, session: Session, *, offset: int = 0, limit: int = 100
    ) -> Sequence[Company]:
        return self.list(session, offset=offset, limit=limit)

    def get_company(self, session: Session, company_id: int) -> Company:
        company = self.get(session, company_id)
        if company is None:
            raise EntityNotFoundError("Company not found")
        return company

    def get_company_including_deleted(
        self, session: Session, company_id: int
    ) -> Company | None:
        return self.soft_repo.get_including_deleted(session, company_id)

    def create_company(self, session: Session, data: CompanyCreate) -> Company:
        company = Company(**data.model_dump())
        return self.create(session, company)

    def update_company(
        self, session: Session, company: Company, data: CompanyUpdate
    ) -> Company:
        values = data.model_dump(exclude_unset=True)
        return self.update(session, company, values)
