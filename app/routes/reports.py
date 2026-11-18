from fastapi import APIRouter, Depends, status

import app.services.reports as report_service

from app.routes.schemas.ReportDataRequest import ReportDataRequest
from app.routes.schemas.ReportDataResponse import ReportDataResponse
from app.utils.auth import get_current_user_name

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    responses={
        401: {
            "description": "Invalid or missing authentication token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid or missing authentication token"
                    }
                },
            },
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "message": "An internal server error occurred."
                    }
                },
            },
        },
    },
)


@router.post(
    "",
    response_model=ReportDataResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_report_data(
    report_data: ReportDataRequest,
    user_name: str = Depends(get_current_user_name),
) -> ReportDataResponse:
    """
    Saves the reason given by an authenticated user to download a report
    from the search module. The user name is taken from the access token.
    """
    return await report_service.add_report_data(report_data, user_name)
