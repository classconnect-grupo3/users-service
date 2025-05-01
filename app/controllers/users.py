# Store user location
from fastapi import APIRouter, Depends, HTTPException, Request
from pytest import Session

from app.common.result import Failure
from app.database.db import get_db
from app.models.user_model import User
from app.schemas.error_response import ErrorResponse
from app.schemas.location import Location
from app.services.users import (
    extract_token_from_request,
    store_location,
    get_user_profile,
    update_user_profile,
)
from app.schemas.user import UserProfileResponse, UserProfileData

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

    result = store_location(db, location.latitude, location.longitude, token)
    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)


@router.get(
    "/me",
    response_model=UserProfileResponse,
    status_code=200,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
)
def get_current_user_profile(
    request: Request,
    db: Session = Depends(get_db),
):
    result = extract_token_from_request(request)

    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    token = result.value

    result = get_user_profile(db, token)

    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    user: User = result.value
    profile_data = UserProfileData.from_orm(user)

    return UserProfileResponse(data=profile_data)


@router.patch(
    "/me",
    response_model=UserProfileResponse,
    status_code=200,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Email already in use by another user",
        },
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
)
def update_current_user_profile(
    update_data: UserProfileData,
    request: Request,
    db: Session = Depends(get_db),
):
    result = extract_token_from_request(request)

    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    token = result.value

    result = update_user_profile(db, update_data, token)

    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    user: User = result.value
    profile_data = UserProfileData.from_orm(user)

    return UserProfileResponse(data=profile_data)
