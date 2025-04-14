# Store user location
from fastapi import APIRouter, Depends, HTTPException, Request
from pytest import Session

from app.common.result import Failure
from app.database.db import get_db
from app.schemas.location import Location
from app.services.users import extract_token_from_request, store_location

router = APIRouter()


@router.post("/me/location")
def store_user_location(
    location: Location,
    request: Request,
    db: Session = Depends(get_db),
):
    result = extract_token_from_request(request)

    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    token = result.value

    result = store_location(db, location, token)
    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)
