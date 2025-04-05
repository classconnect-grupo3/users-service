from sqlalchemy.orm import Session
from app.models.models import Course as DBCourse
from app.schemas.course import CourseBase


# Create a course in the database
def db_create_course(db: Session, course: CourseBase):
    db_course = DBCourse(title=course.title, description=course.description)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


# Get all courses from the database
def db_get_courses(db: Session):
    return db.query(DBCourse).all()