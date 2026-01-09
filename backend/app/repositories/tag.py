from app.models.tag import Tag
from .base import BaseRepository


class TagRepository(BaseRepository[Tag]):
    def __init__(self):
        super().__init__(Tag)
