from app.models.models import MetricInfo


async def get_metric_info_by_metric(metric_name: str):
    return await MetricInfo.filter(metric__name=metric_name)
