from logging import getLogger

from app.models.models import ReportData
from app.utils import context_vars

logger = getLogger(__name__)
request_id_context = context_vars.request_id_context


async def create_report_data(
    user_name: str, description: str, data: str | None = None
) -> ReportData:
    """
    Create a new report data record in the DB.
    """
    report_data = await ReportData.create(
        user_name=user_name, description=description, data=data
    )

    logger.info(
        f"Report data {report_data.id} inserted into the database.",
        extra={"request_id": request_id_context.get()},
    )

    return report_data
