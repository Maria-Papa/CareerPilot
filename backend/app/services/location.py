from sqlalchemy.orm import Session
from app.models import Location
from app.repositories import LocationRepository
from app.schemas import LocationCreate, LocationUpdate
from app.services import BaseService


class LocationService(BaseService[Location]):
    repository: LocationRepository

    def __init__(self):
        super().__init__(LocationRepository())

    def create_location(self, session: Session, data: LocationCreate) -> Location:
        location = Location(**data.model_dump())
        return self.create(session, location)

    def update_location(
        self, session: Session, location: Location, data: LocationUpdate
    ) -> Location:
        values = data.model_dump(exclude_unset=True)
        return self.update(session, location, values)
