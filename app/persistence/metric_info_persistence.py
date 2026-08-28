from typing import List
from app.models.models import MetricInfo

async def get_metric_info_by_metric(metric_name: str) -> List[MetricInfo]:
    """Return all MetricInfo records associated with a metric."""
    return await MetricInfo.filter(metric__name=metric_name)
