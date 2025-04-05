from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.service import (
    create_new_course,
    get_all_courses,
)
from app.schemas.course import CourseBase, CourseResponse, AllCoursesResponse
from app.config.database.db import get_db
from app.schemas.error_response import ErrorResponse

router = APIRouter()


# Create a new course (POST request)
@router.post(
    "/",
    status_code=201,
    responses={
        201: {"description": "Course created successfully", "model": CourseResponse},
        400: {"description": "Bad request error", "model": ErrorResponse},
    },
)
def create_course(course: CourseBase, db: Session = Depends(get_db)):

    course = create_new_course(db=db, course=course)

    return {"data": course}


# Get all courses (GET request)
@router.get(
    "/",
    response_model=AllCoursesResponse,
    responses={
        200: {"description": "A list of courses", "model": AllCoursesResponse},
    },
)
def get_courses(db: Session = Depends(get_db)):

    courses = get_all_courses(db=db)

    return {"data": courses}