from app.models.location import Location
from .base import BaseRepository


class LocationRepository(BaseRepository[Location]):
    def __init__(self):
        super().__init__(Location)
