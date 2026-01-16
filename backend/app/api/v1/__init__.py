from fastapi import APIRouter

from .company import router as companies_router
from .cost_of_living import router as cost_of_living_router
from .currency import router as currencies_router
from .location import router as locations_router

router = APIRouter()
router.include_router(companies_router)
router.include_router(cost_of_living_router)
router.include_router(currencies_router)
router.include_router(locations_router)
