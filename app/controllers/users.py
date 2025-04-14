# Store user location
from fastapi import APIRouter, Depends, HTTPException, Request
from pytest import Session

from app.common.result import Failure
from app.database.db import get_db
from app.schemas.error_response import ErrorResponse
from app.schemas.location import Location
from app.services.users import extract_token_from_request, store_location

router = APIRouter()


@router.post(
    "/me/location",
    status_code=200,
    responses={
        200: {"description": "Location stored successfully"},
        400: {
            "description": "Bad request. For example, UID not found in token.",
            "model": ErrorResponse,
        },
        401: {
            "description": "Unauthorized. Possible reasons include:\n"
            "- Token has expired.\n"
            "- Token has been revoked.\n"
            "- Invalid token.\n"
            "- Invalid email or password.",
            "model": ErrorResponse,
        },
        500: {
            "description": "Internal server error.",
            "model": ErrorResponse,
        },
    },
)
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

    result = store_location(db, location.country, token)
    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)
