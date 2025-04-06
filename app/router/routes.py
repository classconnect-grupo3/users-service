from fastapi import APIRouter
from app.controllers.controller import router as users_router

router = APIRouter()


# Include users router
router.include_router(users_router, prefix="/users", tags=["users"])