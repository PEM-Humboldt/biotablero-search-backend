from logging import getLogger
import fastapi

from app.middleware.exceptions import (
    CollectionNotFoundError,
    ItemsNotFoundError,
    NoFeaturesError,
    HTTPRequestError,
    BBoxValidationError,
)
from app.utils import context_vars

logger = getLogger(__name__)
request_id_context = context_vars.request_id_context


error_messages = {
    404: {
        "collection_not_found": "Collection not found at URL: {url}",
        "items_not_found": "Items not found at URL: {url}",
        "no_features": "No features found in the items data at URL: {url}",
        "no_assets": "No assets found in the first item at URL: {url}",
        "no_valid_asset": "No valid asset found in the first item at URL: {url}",
        "no_href": "No 'href' found in the first asset.",
    },
    500: {"http_error": "HTTP error occurred while accessing {url}"},
    422: {
        "literal_error": "Validation error occurred: {input} at {loc}.",
        "bbox_length": "Bounding box (bbox) must have 4 or 6 elements.",
        "bbox_longitude": "Longitude values must be between -180 and 180.",
        "bbox_latitude": "Latitude values must be between -90 and 90.",
        "bbox_min_max_longitude": "Minimum longitude cannot be greater than maximum longitude.",
        "bbox_min_max_latitude": "Minimum latitude cannot be greater than maximum latitude.",
        "bbox_min_max_altitude": "Minimum altitude cannot be greater than maximum altitude.",
    },
}


def raise_http_exception(status_code: int, error_key: str, url: str):
    error_detail_template = error_messages.get(status_code, {}).get(
        error_key, "Unknown error occurred at URL: {url}"
    )
    error_detail = error_detail_template.format(url=url)

    logger.error(
        f"Error: {error_detail_template} - Path: {url} - Method: 'POST'",
        extra={"request_id": request_id_context.get()},
    )

    raise fastapi.HTTPException(
        status_code=status_code, detail={"message": error_detail}
    )


async def collection_not_found_exception_handler(request, exc):
    error_detail = (
        error_messages.get(404, {})
        .get("collection_not_found")
        .format(url=exc.collection_url)
    )

    logger.error(
        f"Collection not found: {error_detail} - Path: {exc.collection_url} - Method: {request.method}",
        extra={"request_id": request_id_context.get()},
    )

    return fastapi.responses.JSONResponse(
        status_code=404,
        content={"message": error_detail},
    )


async def items_not_found_exception_handler(request, exc):
    error_detail = (
        error_messages.get(404, {})
        .get("items_not_found")
        .format(url=exc.items_url)
    )

    logger.error(
        f"Items not found: {error_detail} - Path: {exc.items_url} - Method: {request.method}",
        extra={"request_id": request_id_context.get()},
    )

    return fastapi.responses.JSONResponse(
        status_code=404,
        content={"message": error_detail},
    )


async def no_features_exception_handler(request, exc):
    error_detail = (
        error_messages.get(404, {})
        .get("no_features")
        .format(url=exc.items_url)
    )

    logger.error(
        f"No features found: {error_detail} - Path: {exc.items_url} - Method: {request.method}",
        extra={"request_id": request_id_context.get()},
    )

    return fastapi.responses.JSONResponse(
        status_code=404,
        content={"message": error_detail},
    )


async def http_request_exception_handler(request, exc):
    error_detail = (
        error_messages.get(500, {}).get("http_error").format(url=exc.url)
    )

    logger.error(
        f"HTTP request error: {error_detail} - Path: {exc.url} - Method: {request.method}",
        extra={"request_id": request_id_context.get()},
    )

    return fastapi.responses.JSONResponse(
        status_code=500,
        content={"message": error_detail},
    )


async def bbox_validation_exception_handler(request, exc):
    error_detail = f"BBox validation error: {exc.message} - BBox: {exc.bbox}"

    logger.error(
        f"BBox validation error: {error_detail} - Path: {request.url} - Method: {request.method}",
        extra={"request_id": request_id_context.get()},
    )

    return fastapi.responses.JSONResponse(
        status_code=422,
        content={"message": error_detail},
    )
