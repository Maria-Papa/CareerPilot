from app.models import Tag
from app.repositories import BaseRepository


class TagRepository(BaseRepository[Tag]):
    def __init__(self):
        super().__init__(Tag)
