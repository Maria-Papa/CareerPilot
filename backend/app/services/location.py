from typing import Sequence

from app.core.errors import EntityNotFoundError
from app.models import Location
from app.repositories import LocationRepository
from app.schemas import LocationCreate, LocationUpdate
from app.services import BaseService
from sqlalchemy.orm import Session


class LocationService(BaseService[Location]):
    def __init__(self, repository: LocationRepository | None = None) -> None:
        repository = repository or LocationRepository()
        super().__init__(repository)

    def list_locations(
        self, session: Session, *, offset: int = 0, limit: int = 100
    ) -> Sequence[Location]:
        return self.list(session, offset=offset, limit=limit)

    def get_location(self, session: Session, location_id: int) -> Location:
        location = self.get(session, location_id)
        if location is None:
            raise EntityNotFoundError("Location not found")
        return location

    def create_location(self, session: Session, data: LocationCreate) -> Location:
        location = Location(**data.model_dump())
        return self.create(session, location)

    def update_location(
        self, session: Session, location: Location, data: LocationUpdate
    ) -> Location:
        values = data.model_dump(exclude_unset=True)
        return self.update(session, location, values)
