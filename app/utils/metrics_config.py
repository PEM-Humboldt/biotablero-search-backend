from typing import List

from fastapi import HTTPException

from app.middleware.exceptions import UnsupportedMetricException
from app.routes.schemas.MetricResponse import METRICS_CONFIG


def metric_group_key(metric_id: str) -> str:
    """
    Retrieves the group key used to aggregate data for a given metric.

    Args:
        metric_id (str): The identifier of the metric.

    Returns:
        str: The group key associated with the metric (e.g., 'ano', 'periodo').

    Raises:
        ValueError: If no group key is defined for the given metric_id.
    """
    group_key = METRICS_CONFIG.get(metric_id, {}).get("group_key")
    if group_key is None:
        raise ValueError(f"No group_key defined for metric_id '{metric_id}'")
    return group_key


def build_metric_response(metric_id: str, values: List[dict]) -> List[dict]:
    """
    Converts a list of raw dictionaries into instances of the configured Pydantic model
    for a specific metric, and serializes them into dictionaries for response.

    Args:
        metric_id (str): The identifier of the metric.
        values (List[dict]): The raw data values to convert.

    Returns:
        List[dict]: A list of serialized model instances matching the metric's structure.

    Raises:
        HTTPException: If the metric_id is unsupported or misconfigured.
    """
    model = METRICS_CONFIG.get(metric_id, {}).get("model")
    if not model:
        raise UnsupportedMetricException(metric_id)

    return [model(**item).model_dump() for item in values]
