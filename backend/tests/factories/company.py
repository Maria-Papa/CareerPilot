from app.models.company import Company
from sqlalchemy.orm import Session


def create_company(db_session: Session, **kwargs) -> Company:
    defaults = {
        "name": "Company",
        "website": None,
        "industry": None,
        "logo_url": None,
    }
    defaults.update(kwargs)

    company = Company(**defaults)
    db_session.add(company)
    db_session.commit()
    db_session.refresh(company)
    return company
