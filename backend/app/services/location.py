from app.models import Location
from app.repositories import LocationRepository
from app.schemas import LocationCreate, LocationUpdate
from app.services import BaseService
from sqlalchemy.orm import Session


class LocationService(BaseService[Location]):
    def __init__(self):
        super().__init__(LocationRepository())

    def list_locations(self, session: Session):
        return self.list(session)

    def create_location(self, session: Session, data: LocationCreate) -> Location:
        location = Location(**data.model_dump())
        return self.create(session, location)

    def update_location(
        self, session: Session, location: Location, data: LocationUpdate
    ) -> Location:
        values = data.model_dump(exclude_unset=True)
        return self.update(session, location, values)
