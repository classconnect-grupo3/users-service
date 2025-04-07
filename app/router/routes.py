from fastapi import APIRouter
from app.controllers.register_controller import router as register_users_router

router = APIRouter()


# Include users router
router.include_router(register_users_router, prefix="/register", tags=["register"])
