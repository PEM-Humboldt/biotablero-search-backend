import fastapi

from app.utils import context_vars
from uuid import uuid4
from logging import getLogger

logger = getLogger(__name__)
request_id_context = context_vars.request_id_context


async def log_requests(request: fastapi.Request, call_next):
    request_id = str(uuid4())
    request_id_context.set(request_id)

    logger.info(
        f"Method: {request.method} - URL: {request.url}",
        extra={"request_id": request_id},
    )

    response = await call_next(request)
    logger.info(
        f"Response status: {response.status_code}",
        extra={"request_id": request_id},
    )
    return response
