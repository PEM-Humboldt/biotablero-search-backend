from logging import getLogger

from fastapi import FastAPI, exceptions
from fastapi.middleware.cors import CORSMiddleware

from app.middleware.exception_handlers import (
    validation_exception_handler,
    server_exception_handler,
    not_found_exception_handler,
)
from app.middleware.exceptions import UnsupportedMetricException

from app.utils.errors import ServerError, NotFoundError, UnprocessableError
from app.middleware.log_middleware import log_requests
from app.routes import metrics, areas, health
from app.utils.config import get_settings, TORTOISE_ORM
from tortoise.contrib.fastapi import register_tortoise

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

app.middleware("http")(log_requests)

app.add_exception_handler(
    exceptions.RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    exceptions.ValidationException,
    validation_exception_handler,
)

app.add_exception_handler(NotFoundError, not_found_exception_handler)
app.add_exception_handler(ServerError, server_exception_handler)
app.add_exception_handler(UnprocessableError, server_exception_handler)
app.add_exception_handler(Exception, server_exception_handler)
app.add_exception_handler(UnsupportedMetricException, server_exception_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(metrics.router)
app.include_router(areas.router)
app.include_router(health.router)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
