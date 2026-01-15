from app.models import CostOfLiving
from sqlalchemy.orm import Session


def create_cost_of_living(db_session: Session, **kwargs) -> CostOfLiving:
    defaults = {
        "location_id": 1,
        "yearly_cost": 500000,
        "title": "Default COL",
    }
    defaults.update(kwargs)

    col = CostOfLiving(**defaults)
    db_session.add(col)
    db_session.commit()
    db_session.refresh(col)
    return col
