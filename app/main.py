from logging import getLogger

from fastapi import FastAPI, exceptions
from app.middleware.exception_handlers import (
    validation_exception_handler,
    server_exception_handler,
    not_found_exception_handler,
)
from app.utils.errors import ServerError, NotFoundError
from app.middleware.log_middleware import log_requests
from app.routes import metrics
from app.utils import context_vars
from app.utils.config import get_settings

settings = get_settings()
settings.configure_logging()
logger = getLogger(__name__)
request_id_context = context_vars.request_id_context

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
app.add_exception_handler(Exception, server_exception_handler)

app.include_router(metrics.router)
