from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from app.schemas.error_response import ErrorResponse


def configure_exception_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_error_handler(request: Request, exc: HTTPException):
        title = exc.headers.get("X-Error", "Error") if exc.headers else "Error"
        error_response = ErrorResponse(
            type="https://example.com/errors/" + exc.detail.replace(" ", "-").lower(),
            title=title,
            status=exc.status_code,
            detail=exc.detail,
            instance=str(request.url),
        )
        return JSONResponse(
            status_code=exc.status_code, content=error_response.model_dump()
        )
