from fastapi import APIRouter

from app.controllers.register import router as register_users_router
from app.controllers.users import router as users_router
from app.controllers.login_with_email import router as login_email_router
from app.controllers.login_with_google import router as login_google_router


router = APIRouter()


router.include_router(register_users_router, prefix="/register", tags=["register"])
router.include_router(users_router, prefix="/users", tags=["users"])


router.include_router(login_email_router, prefix="/login/email", tags=["login"])
router.include_router(login_google_router, prefix="/login/google", tags=["login"])
