from logging import getLogger

import fastapi
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routes import metrics
from app.utils import context_vars, exception_handlers, middleware
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

app.middleware("http")(middleware.log_requests)

app.add_exception_handler(StarletteHTTPException, exception_handlers.http_exception_handler)
app.add_exception_handler(fastapi.exceptions.RequestValidationError, exception_handlers.validation_exception_handler)

app.include_router(metrics.router)
# TODO: disable swagger on production: https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls
