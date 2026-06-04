from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.backend.exception.app_exceptions import AppException

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def handle_app_exception(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )