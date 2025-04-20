from fastapi import APIRouter

from app.controllers.login_with_email import router as login_users_router
from app.controllers.register import router as register_users_router
from app.controllers.users import router as users_router


router = APIRouter()


router.include_router(register_users_router, prefix="/register", tags=["register"])
router.include_router(login_users_router, prefix="/login", tags=["login"])
router.include_router(users_router, prefix="/users", tags=["users"])
