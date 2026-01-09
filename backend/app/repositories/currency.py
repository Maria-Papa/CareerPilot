from app.models.currency import Currency
from .base import BaseRepository


class CurrencyRepository(BaseRepository[Currency]):
    def __init__(self):
        super().__init__(Currency)
