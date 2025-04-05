from fastapi import APIRouter
from app.controllers.controller import router as courses_router

router = APIRouter()


# Include Courses router
router.include_router(courses_router, prefix="/courses", tags=["courses"])