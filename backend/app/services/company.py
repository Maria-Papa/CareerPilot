from sqlalchemy.orm import Session
from app.models import Company
from app.repositories import CompanyRepository
from app.schemas import CompanyCreate, CompanyUpdate
from app.services import BaseService


class CompanyService(BaseService[Company]):
    repository: CompanyRepository

    def __init__(self):
        super().__init__(CompanyRepository())

    def create_company(self, session: Session, data: CompanyCreate) -> Company:
        company = Company(**data.model_dump())
        return self.create(session, company)

    def update_company(
        self, session: Session, company: Company, data: CompanyUpdate
    ) -> Company:
        values = data.model_dump(exclude_unset=True)
        return self.update(session, company, values)

    def deactivate_company(self, session: Session, company: Company) -> Company:
        company.is_deleted = True
        return self.update(session, company, {"is_deleted": True})

    def reactivate_company(self, session: Session, company: Company) -> Company:
        company.is_deleted = False
        return self.update(session, company, {"is_deleted": False})
