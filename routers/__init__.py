from fastapi import APIRouter
from .users import router as users_router
from .favorites import router as favorites_router

router = APIRouter()

router.include_router(users_router, prefix='/users', tags=['users'])
router.include_router(favorites_router, prefix='/favorites', tags=['users'])