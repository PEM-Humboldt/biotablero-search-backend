from logging import getLogger

import fastapi
from app.middleware.exception_handlers import (
    validation_exception_handler,
    generic_exception_handler,
)
from app.middleware.exceptions import (
    CollectionNotFoundError,
    ItemsNotFoundError,
    NoFeaturesError,
    HTTPRequestError,
    BBoxValidationError,
)
from app.middleware.log_middleware import log_requests
from app.routes import metrics
from app.utils import context_vars
from app.utils.config import get_settings
from app.utils.errors import (
    collection_not_found_exception_handler,
    items_not_found_exception_handler,
    no_features_exception_handler,
    http_request_exception_handler,
    bbox_validation_exception_handler,
)

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

app.add_exception_handler(
    CollectionNotFoundError, collection_not_found_exception_handler
)
app.add_exception_handler(
    ItemsNotFoundError, items_not_found_exception_handler
)
app.add_exception_handler(NoFeaturesError, no_features_exception_handler)
app.add_exception_handler(HTTPRequestError, http_request_exception_handler)
app.add_exception_handler(
    BBoxValidationError, bbox_validation_exception_handler
)
app.add_exception_handler(
    fastapi.exceptions.RequestValidationError, validation_exception_handler
)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(metrics.router)
# TODO: disable swagger on production: https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls
