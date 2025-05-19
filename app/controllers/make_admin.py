from fastapi import APIRouter, Depends, HTTPException
from app.schemas.email import Email
from app.services.make_admin import make_admin_by
from sqlalchemy.orm import Session

from app.common.result import Failure
from app.database.db import get_db
from app.errors.register_errors import CouldNotCreateFirebaseUser, UserAlreadyExists
from app.schemas.user import UserBase
from app.services.register import create_new_user
from app.common.http_responses.register import register_responses

router = APIRouter()


# Create a new user (POST request)
@router.post("", status_code=201, responses=register_responses)
def make_admin(request: Email, db: Session = Depends(get_db)):

    result = make_admin_by(request.email, db)
    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)
    return {"data": result.value}
