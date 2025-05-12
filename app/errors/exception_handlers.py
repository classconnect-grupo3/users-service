from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.error_response import ErrorResponse


def configure_exception_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_error_handler(request: Request, exc: HTTPException):
        title = exc.headers.get("X-Error", "Error") if exc.headers else "Error"
        error_response = ErrorResponse(
            type="https://example.com/errors/"
            + (
                exc.detail.replace(" ", "-").lower()
                if isinstance(exc.detail, str)
                else "unknown-error"
            ),
            title=title,
            status=exc.status_code,
            detail=exc.detail,
            instance=str(request.url),
        )
        return JSONResponse(
            status_code=exc.status_code, content=error_response.model_dump()
        )
    
    # @app.exception_handler(RequestValidationError)
    # async def validation_error_handler(request: Request, exc: RequestValidationError):
    #     error_response = ErrorResponse(
    #         type="https://example.com/errors/validation-error",
    #         title="Validation Error",
    #         status=422,
    #         detail=str(exc),
    #         instance=str(request.url),
    #     )
    #     return JSONResponse(
    #         status_code=422, content=error_response.model_dump()
    #     )

    # @app.exception_handler(SQLAlchemyError)
    # async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    #     error_response = ErrorResponse(
    #         type="https://example.com/errors/database-error",
    #         title="Database Error",
    #         status=500,
    #         detail="A database error occurred.",
    #         instance=str(request.url),
    #     )
    #     return JSONResponse(
    #         status_code=500, content=error_response.model_dump()
    #     )

    # @app.exception_handler(Exception)
    # async def generic_error_handler(request: Request, exc: Exception):
    #     error_response = ErrorResponse(
    #         type="https://example.com/errors/internal-server-error",
    #         title="Internal Server Error",
    #         status=500,
    #         detail="An unexpected error occurred.",
    #         instance=str(request.url),
    #     )
    #     return JSONResponse(
    #         status_code=500, content=error_response.model_dump()
    #     )