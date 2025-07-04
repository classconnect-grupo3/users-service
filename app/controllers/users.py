# Store user location
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Optional
from app.schemas.email import Email
from pydantic import EmailStr
from app.schemas.query import Query
from pytest import Session
from app.common.http_responses.make_admin import make_admin_response
from app.common.http_responses.block_user import block_user_response
from app.common.http_responses.unlock_user import unlock_user_response
from app.common.http_responses.is_active import is_active_response
from app.schemas.user import UserStatsData

from app.common.result import Failure
from app.database.db import get_db
from app.models.user_model import User
from app.schemas.error_response import ErrorResponse
from app.schemas.location import Location
from app.services.users import (
    block_user_by,
    extract_token_from_request,
    make_admin_by,
    send_password_reset_link,
    store_location,
    get_user_profile,
    update_user_profile_service,
    search_users_service,
    get_user_by_id_service,
    get_users_batch_service,
    get_user_stats_service,
    unlock_user_by,
    is_user_active_by_email,
    is_user_admin_by_uid,
)
from app.schemas.user import (
    UserProfileResponse,
    UserProfileData,
    UserProfileUpdate,
    UsersSearchResponse,
    UsersBatchRequest,
    UserStatsResponse,
    UserIsActiveResponse,
    UserIsAdminResponse,
)
from app.common.http_responses.forgot_password import forgot_password_responses
from app.common.http_responses.is_admin import is_admin_response

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
def update_user_profile(
    request: Request,
    update_data: UserProfileUpdate,
    db: Session = Depends(get_db),
):
    result = extract_token_from_request(request)

    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    token = result.value

    result = update_user_profile_service(db, update_data, token)

    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    user: User = result.value
    profile_data = UserProfileData.from_orm(user)

    return UserProfileResponse(data=profile_data)


@router.get(
    "/search",
    response_model=UsersSearchResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {
            "model": ErrorResponse,
            "description": "No users found matching your search",
        },
        500: {"model": ErrorResponse, "description": "Server error"},
    },
)
def search_users(
    query: str,
    request: Request,
    db: Session = Depends(get_db),
):
    result = extract_token_from_request(request)
    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    result = search_users_service(db, query)

    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    users = result.value

    user_profiles = [UserProfileData.from_orm(user) for user in users]

    return UsersSearchResponse(data=user_profiles)


@router.get(
    "/{user_id}",
    response_model=UserProfileResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "User not found"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
)
def get_user_by_id(
    user_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    # result = extract_token_from_request(request)
    # if isinstance(result, Failure):
    #     error = result.error
    #     raise HTTPException(status_code=error.http_status_code, detail=error.message)

    result = get_user_by_id_service(db, user_id)

    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    user: User = result.value
    profile_data = UserProfileData.from_orm(user)

    return UserProfileResponse(data=profile_data)


@router.post(
    "/batch",
    response_model=UsersSearchResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {
            "model": ErrorResponse,
            "description": "No users found for the provided IDs",
        },
        500: {"model": ErrorResponse, "description": "Server error"},
    },
)
def get_users_batch(
    request_data: UsersBatchRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    result = extract_token_from_request(request)
    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    result = get_users_batch_service(db, request_data.user_ids)

    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    users = result.value

    user_profiles = [UserProfileData.from_orm(user) for user in users]

    return UsersSearchResponse(data=user_profiles)


@router.post("/admin", status_code=201, responses=make_admin_response)
def make_admin(request: Email, db: Session = Depends(get_db)):

    result = make_admin_by(request.email, db)
    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    user: User = result.value
    profile_data = UserProfileData.model_validate(user)

    return UserProfileResponse(data=profile_data)


@router.post("/block", status_code=201, responses=block_user_response)
def block_user(request: Email, db: Session = Depends(get_db)):

    result = block_user_by(request.email, db)
    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    user: User = result.value
    profile_data = UserProfileData.model_validate(user)

    return UserProfileResponse(data=profile_data)


@router.post("/unlock", status_code=201, responses=unlock_user_response)
def unlock_user(request: Email, db: Session = Depends(get_db)):
    result = unlock_user_by(request.email, db)
    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    user: User = result.value
    profile_data = UserProfileData.model_validate(user)

    return UserProfileResponse(data=profile_data)


@router.post(
    "/forgot-password",
    status_code=202,
    responses=forgot_password_responses,
)
async def forgot_password(request: Email):
    result = await send_password_reset_link(request.email)
    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)
    return {"message": result.value}


# Admin endpoints
@router.get(
    "/admin/stats",
    response_model=UserStatsResponse,
    status_code=200,
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Unauthorized or admin permissions required",
        },
        500: {"model": ErrorResponse, "description": "Server error"},
    },
)
def get_user_stats(
    request: Request,
    db: Session = Depends(get_db),
):
    result = extract_token_from_request(request)

    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    token = result.value
    result = get_user_stats_service(db, token)

    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    stats = result.value
    stats_data = UserStatsData(**stats)

    return UserStatsResponse(data=stats_data)


@router.get(
    "/{email}/is-active",
    status_code=200,
    response_model=UserIsActiveResponse,
    responses=is_active_response,
)
def is_user_active(email: str, db: Session = Depends(get_db)):
    result = is_user_active_by_email(email, db)
    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    is_active = result.value

    return UserIsActiveResponse(is_active=is_active)


@router.get(
    "/{user_id}/is-admin",
    status_code=200,
    response_model=UserIsAdminResponse,
    responses=is_admin_response,
)
def is_user_admin(user_id: str, db: Session = Depends(get_db)):
    result = is_user_admin_by_uid(user_id, db)
    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    user_data = result.value
    return UserIsAdminResponse(is_admin=user_data["is_admin"], email=user_data["email"])
