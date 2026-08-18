from app.models.models import MetricInfo


async def get_metric_info_by_metric_id(metric_id: int):
    return await MetricInfo.filter(metric_id=metric_id).order_by("id")
