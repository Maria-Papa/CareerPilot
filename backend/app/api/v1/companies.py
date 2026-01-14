# backend/app/api/v1/companies.py
from typing import List

from app.api import get_entity_or_404
from app.db import get_session
from app.schemas.company import CompanyCreate, CompanyRead, CompanyUpdate
from app.services.company import CompanyService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/companies", tags=["companies"])

company_service = CompanyService()

get_company_or_404 = get_entity_or_404(company_service.get_company_including_deleted)
get_active_company_or_404 = get_entity_or_404(company_service.get_company)


@router.get("", response_model=List[CompanyRead])
def list_companies(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    return company_service.list_companies(session, offset=offset, limit=limit)


@router.get(
    "/{company_id}", response_model=CompanyRead
)  # TODO: What to do with soft deleted companies?
def get_company(company=Depends(get_active_company_or_404)):
    return company


@router.post("", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
def create_company(data: CompanyCreate, session: Session = Depends(get_session)):
    return company_service.create_company(session, data)


@router.patch(
    "/{company_id}", response_model=CompanyRead
)  # TODO: What to do with soft deleted companies?
def update_company(
    data: CompanyUpdate,
    company=Depends(get_active_company_or_404),
    session: Session = Depends(get_session),
):
    return company_service.update_company(session, company, data)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(
    company=Depends(get_active_company_or_404), session: Session = Depends(get_session)
):
    company_service.delete(session, company)
    return None


@router.post("/{company_id}/restore", response_model=CompanyRead)
def restore_company(
    company=Depends(get_company_or_404), session: Session = Depends(get_session)
):
    company_service.restore(session, company)
    return company
