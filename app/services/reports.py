from app.routes.schemas.ReportDataRequest import ReportDataRequest
from app.routes.schemas.ReportDataResponse import ReportDataResponse

from app.persistence.report_data_persistence import create_report_data


async def add_report_data(
    report_data: ReportDataRequest,
    user_name: str,
) -> ReportDataResponse:
    """
    Saves the reason given by a user to download a report.
    """
    report_data_obj = await create_report_data(
        user_name, report_data.description
    )

    return ReportDataResponse(
        id=report_data_obj.id,
        creation_date=report_data_obj.creation_date,
        user_name=report_data_obj.user_name,
        description=report_data_obj.description,
    )
