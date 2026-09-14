from app.models.models import Metric, MetricCollection
from app.utils.errors import NotFoundError


def get_collection_by_group(
    metric: Metric, group: str | None
) -> MetricCollection | None:
    """
    Returns the MetricCollection matching the given group among the
    metric's already-loaded collections, falling back to the primary
    collection when no group is provided (group == "total").
    """
    if group and group != "total":
        collection = next(
            (mc for mc in metric.collections if mc.group_name == group), None
        )
        if collection is None:
            raise NotFoundError(
                usr_msg=(
                    f"Group '{group}' not found for metric "
                    f"'{metric.name}'."
                ),
                log_msg=(
                    f"No MetricCollection with group_name='{group}' found "
                    f"for metric {metric.name}."
                ),
            )
        return collection
    return next((mc for mc in metric.collections if mc.is_primary), None)
