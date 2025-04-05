from typing import List
import uuid
from pydantic import BaseModel


class CourseBase(BaseModel):
    title: str
    description: str


# Pydantic model for returning the course data with ID
class Course(CourseBase):
    id: uuid.UUID

    class Config:
        from_attributes = (
            True  # Tells Pydantic to treat the SQLAlchemy model as a dictionary
        )

class AllCoursesResponse(BaseModel):
    data: List[Course]

class CourseResponse(BaseModel):
    data: Course