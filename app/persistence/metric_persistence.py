from app.models.models import Metric


async def get_metric_by_name(
    metric_name: str,
) -> Metric | None:
    """
    Get Metric object by short name.
    """
    return await Metric.get_or_none(name=metric_name).prefetch_related(
        "collections", "indicator", "info"
    )


def normalize_metric_group(metric: Metric, group: str | None) -> str:
    """
    Returns the requested group only if the metric actually supports groups,
    otherwise returns "total".
    """
    indicator = next(iter(metric.indicator), None)
    indicator_has_group = bool(indicator and indicator.has_group)
    collections_have_group = any(
        mc.group_name is not None for mc in metric.collections
    )
    if (indicator_has_group or collections_have_group) and group:
        return group
    return "total"

