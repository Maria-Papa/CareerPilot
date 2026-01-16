from fastapi import APIRouter

from .company import router as companies_router
from .cost_of_living import router as cost_of_living_router
from .currency import router as currencies_router
from .file import router as file_router
from .interview import router as interview_router
from .job import router as jobs_router
from .location import router as locations_router
from .tag import router as tags_router
from .user import router as users_router

router = APIRouter(prefix="/api/v1")

router.include_router(companies_router)
router.include_router(cost_of_living_router)
router.include_router(currencies_router)
router.include_router(file_router)
router.include_router(interview_router)
router.include_router(jobs_router)
router.include_router(locations_router)
router.include_router(tags_router)
router.include_router(users_router)
