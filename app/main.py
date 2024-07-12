import fastapi

from app.routes import metrics
from app.config import get_settings
from logging import getLogger
from starlette.exceptions import HTTPException as StarletteHTTPException
from uuid import uuid4
from app.services.utils import context_vars

settings = get_settings()
settings.configure_logging()
logger = getLogger(__name__)
request_id_context = context_vars.request_id_context

app = fastapi.FastAPI(
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


@app.middleware("http")
async def log_requests(request: fastapi.Request, call_next):
    request_id = str(uuid4())
    request_id_context.set(request_id)

    logger.info(
        f"Method: {request.method} - URL: {request.url}",
        extra={"request_id": request_id},
    )

    response = await call_next(request)
    logger.info(
        f"Response status: {response.status_code }",
        extra={"request_id": request_id},
    )
    return response


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logger.error(
        f"HTTP Exception: {exc} - Path: {request.url} - Method: {request.method}",
        extra={"request_id": request_id_context.get()},
    )
    return fastapi.responses.JSONResponse(
        exc.detail, status_code=exc.status_code
    )


@app.exception_handler(fastapi.exceptions.RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(
        f"Validation error: {exc.errors()} - Path: {request.url} - Method: {request.method}",
        extra={"request_id": request_id_context.get()},
    )
    return fastapi.responses.JSONResponse(
        status_code=422,
        content={"detail": str(exc.errors())},
    )


app.include_router(metrics.router)
# TODO: disable swagger on production: https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls
