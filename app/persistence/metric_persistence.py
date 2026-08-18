from app.models.models import Metric


async def get_metric_by_name(
    metric_name: str,
) -> Metric | None:
    """
    Get Metric object by short name.
    """
    return await Metric.get_or_none(name=metric_name).prefetch_related(
        "collections", "indicator"
    )


async def get_metric_by_id(
    metric_id: int,
) -> Metric | None:
    """
    Get Metric object by id.
    """
    return await Metric.get_or_none(id=metric_id).prefetch_related(
        "collections", "indicator", "info"
    )
