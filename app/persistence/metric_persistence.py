from app.models.models import Metric


async def get_metric_from_short_name(
    metric_name: str,
) -> Metric | None:
    """
    Get Metric object by short name.
    """
    return await Metric.get_or_none(short_name=metric_name).prefetch_related(
        "collection"
    )
