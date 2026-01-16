from app.api.deps import get_entity_or_404
from app.db import get_session
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyRead, CompanyUpdate
from app.services.company import CompanyService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/companies", tags=["companies"])

service = CompanyService()
get_company_or_404 = get_entity_or_404(service.get_company_including_deleted)
get_active_company_or_404 = get_entity_or_404(service.get_company)


@router.get("", response_model=list[CompanyRead])
def list_companies(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    return service.list_companies(session, offset=offset, limit=limit)


@router.get("/{company_id}", response_model=CompanyRead)
def get_company(company: Company = Depends(get_active_company_or_404)):
    return company


@router.post("", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
def create_company(data: CompanyCreate, session: Session = Depends(get_session)):
    return service.create_company(session, data)


@router.patch("/{company_id}", response_model=CompanyRead)
def update_company(
    data: CompanyUpdate,
    company: Company = Depends(get_active_company_or_404),
    session: Session = Depends(get_session),
):
    return service.update_company(session, company, data)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(
    company: Company = Depends(get_active_company_or_404),
    session: Session = Depends(get_session),
):
    service.delete(session, company)
    return None


@router.post("/{company_id}/restore", response_model=CompanyRead)
def restore_company(
    company: Company = Depends(get_company_or_404),
    session: Session = Depends(get_session),
):
    service.restore(session, company)
    return company
