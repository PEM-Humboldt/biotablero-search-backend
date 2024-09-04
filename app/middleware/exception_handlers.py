import traceback

import fastapi
import fastapi.exception_handlers

from app.utils import context_vars
from logging import getLogger

logger = getLogger(__name__)
request_id_context = context_vars.request_id_context


async def validation_exception_handler(request, exc):
    logger.error(
        exc.errors(),
        extra={"request_id": request_id_context.get()},
    )
    return (
        await fastapi.exception_handlers.request_validation_exception_handler(
            request, exc
        )
    )


async def not_found_exception_handler(request, exc):
    logger.error(
        exc.log_msg,
        extra={"request_id": request_id_context.get()},
    )

    return fastapi.responses.JSONResponse(
        status_code=404,
        content={"detail": exc.usr_msg},
    )


async def server_exception_handler(request, exc):
    tb_str = traceback.format_exception(exc.__class__, exc, exc.__traceback__)

    logger.error(
        f"\n{''.join(tb_str)}",
        extra={"request_id": request_id_context.get()},
    )

    code = exc.code if hasattr(exc, "code") else 500
    msg = (
        exc.usr_msg
        if hasattr(exc, "usr_msg")
        else "There was an internal error"
    )
    return fastapi.responses.JSONResponse(
        status_code=code,
        content={"detail": msg},
    )
