import traceback

import fastapi
from app.utils import context_vars
from logging import getLogger
from app.utils.errors import error_messages

logger = getLogger(__name__)
request_id_context = context_vars.request_id_context


async def validation_exception_handler(
    request: fastapi.Request, exc: fastapi.exceptions.RequestValidationError
):
    error_details = exc.errors()

    first_error = error_details[0]
    loc = first_error.get("loc", [])
    expected = first_error.get("type", "unknown")
    input_value = first_error.get("msg", "unknown")

    error_key = "literal_error"
    error_detail_template = error_messages.get(422, {}).get(error_key)

    if error_detail_template:
        error_detail = error_detail_template.format(
            loc=" -> ".join(loc), expected=expected, input=input_value
        )
    else:
        error_detail = "Validation error occurred."

    logger.error(
        f"Validation error: {error_details} - Path: {request.url} - Method: {request.method}",
        extra={"request_id": request_id_context.get()},
    )

    return fastapi.responses.JSONResponse(
        status_code=422,
        content={"message": error_detail},
    )


async def generic_exception_handler(request: fastapi.Request, exc: Exception):
    tb_str = traceback.format_exception(exc.__class__, exc, exc.__traceback__)

    logger.error(
        f"Unhandled Exception: {str(exc)} - Path: {request.url} - Method: {request.method} - Traceback:\n{''.join(tb_str)}",
        extra={"request_id": request_id_context.get()},
    )
    return fastapi.responses.JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred."},
    )
