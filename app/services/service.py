from sqlalchemy.orm import Session
from app.repositories.repository import (
    db_create_course,
    db_get_courses,
)
from app.schemas.course import CourseBase, Course


# Service to create a course
def create_new_course(db: Session, course: CourseBase) -> Course:
    return db_create_course(db=db, course=course)


# Service to get all courses
def get_all_courses(db: Session):
    return db_get_courses(db=db)