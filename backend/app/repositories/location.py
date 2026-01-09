from app.models import Location
from app.repositories import BaseRepository


class LocationRepository(BaseRepository[Location]):
    def __init__(self):
        super().__init__(Location)
