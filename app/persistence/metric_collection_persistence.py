from app.models.models import Metric, MetricCollection


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
