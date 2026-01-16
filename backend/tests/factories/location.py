from app.models.location import Location
from sqlalchemy.orm import Session


def create_location(db_session: Session, **kwargs) -> Location:
    defaults = {
        "name": "Test City",
        "country_code": "SE",
        "currency_id": 1,
    }
    defaults.update(kwargs)

    loc = Location(**defaults)
    db_session.add(loc)
    db_session.commit()
    db_session.refresh(loc)
    return loc
