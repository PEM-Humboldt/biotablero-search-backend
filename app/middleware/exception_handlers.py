import fastapi

from app.utils import context_vars
from logging import getLogger

logger = getLogger(__name__)
request_id_context = context_vars.request_id_context


async def http_exception_handler(request, exc):
    logger.error(
        f"HTTP Exception: {exc} - Path: {request.url} - Method: {request.method}",
        extra={"request_id": request_id_context.get()},
    )
    return fastapi.responses.JSONResponse(
        exc.detail, status_code=exc.status_code
    )


async def validation_exception_handler(request, exc):
    logger.error(
        f"Validation error: {exc.errors()} - Path: {request.url} - Method: {request.method}",
        extra={"request_id": request_id_context.get()},
    )
    return fastapi.responses.JSONResponse(
        status_code=422,
        content={"detail": str(exc.errors())},
    )
