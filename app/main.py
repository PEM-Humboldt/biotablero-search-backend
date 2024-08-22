from logging import getLogger

import fastapi
from app.middleware.exception_handlers import (
    generic_exception_handler,
    validation_exception_handler,
)
from app.middleware.log_middleware import log_requests
from app.routes import metrics
from app.utils import context_vars
from app.utils.config import get_settings

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

app.middleware("http")(log_requests)

app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(
    fastapi.exceptions.RequestValidationError, validation_exception_handler
)

app.include_router(metrics.router)
# TODO: disable swagger on production: https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls
