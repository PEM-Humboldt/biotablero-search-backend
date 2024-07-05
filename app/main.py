from fastapi import FastAPI, exceptions, responses

from app.routes import metrics
from app.config import get_settings
from logging import getLogger
from starlette.exceptions import HTTPException as StarletteHTTPException

settings = get_settings()
settings.configure_logging()
logger = getLogger(__name__)


app = FastAPI(
    title="BioTableroSearch",
    description="Get metrics by predefined or custom (polygon) areas.",
    summary="Metrics for BioTablero Search module",
    version="0.1.0",
    contact={
        "name": "Equipo BioTablero",
        "url": "http://biotablero.humboldt.org.co/",
        "email": "biotablero@humboldt.org.co",
    },
    docs_url=None if settings.env.lower() == "prod" else "/docs",
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logger.error(
        f"HTTP Exception: {exc} - Path: {request.url} - Method: {request.method}"
    )
    return responses.JSONResponse(exc.detail, status_code=exc.status_code)


@app.exception_handler(exceptions.RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(
        f"Validation error: {exc.errors()} - Path: {request.url} - Method: {request.method}"
    )
    return responses.JSONResponse(
        status_code=422,
        content={"detail": str(exc.errors())},
    )


app.include_router(metrics.router)
# TODO: disable swagger on production: https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls
