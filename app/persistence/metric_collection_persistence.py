from app.models.models import Metric, MetricCollection


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


def get_collection_by_group(
    metric: Metric, group: str | None
) -> MetricCollection | None:
    """
    Returns the MetricCollection matching the given group among the
    metric's already-loaded collections, falling back to the primary
    collection when no group is provided (group == "total").
    """
    if group and group != "total":
        return next(
            (mc for mc in metric.collections if mc.group_name == group), None
        )
    return next((mc for mc in metric.collections if mc.is_primary), None)
