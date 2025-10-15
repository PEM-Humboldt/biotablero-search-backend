from typing import List, Dict

from app.middleware.exceptions import UnsupportedMetricException
from app.routes.schemas.MetricResponse import (
    MetricConfig,
    LossPersistenceResponse,
    CoverageResponse,
    HumanFootPrintResponse,
)

METRICS_CONFIG: Dict[str, MetricConfig] = {
    "LossPersistence": {
        "model": LossPersistenceResponse,
        "example": [
            {
                "perdida": 1971.3859302816563,
                "persistencia": 161349.158786824,
                "no_bosque": 192519.67643274338,
                "periodo": "2016-2021",
            },
            {
                "perdida": 1572.6614325195167,
                "persistencia": 162684.80917653913,
                "no_bosque": 191582.75054079038,
                "periodo": "2011-2015",
            },
            {
                "perdida": 844.3758017993621,
                "persistencia": 164716.61720378936,
                "no_bosque": 190279.2281442603,
                "periodo": "2006-2010",
            },
            {
                "perdida": 1164.8889557696975,
                "persistencia": 165904.73952933252,
                "no_bosque": 188770.59266474683,
                "periodo": "2000-2005",
            },
        ],
        "description": "Forest loss and persistence",
        "group_key": "periodo",
    },
    "Coverage": {
        "model": CoverageResponse,
        "example": [
            {
                "ano": "2021",
                "natural": 180000.0,
                "secundaria": 25000.0,
                "transformada": 12000.0,
            }
        ],
        "description": "Land cover",
        "group_key": "ano",
    },
    "CurrentHF": {
        "model": HumanFootPrintResponse,
        "example": [
            {
                "ano": "2021",
                "natural": 1971.38,
                "baja": 161349.15,
                "media": 192519.67,
                "alta": 194312.67,
            }
        ],
        "description": "Human footprint",
        "group_key": "ano",
    },
}


def metric_group_key(metric_name: str) -> str:
    """
    Retrieves the group key used to aggregate data for a given metric.

    Args:
        metric_id (str): The identifier name of the metric.

    Returns:
        str: The group key associated with the metric (e.g., 'ano', 'periodo').

    Raises:
        ValueError: If no group key is defined for the given metric_id.
    """
    group_key = METRICS_CONFIG.get(metric_name, {}).get("group_key")
    if group_key is None:
        raise ValueError(f"No group_key defined for metric_id '{metric_name}'")
    return group_key


def build_metric_response(metric_name: str, values: List[dict]) -> List[dict]:
    """
    Converts a list of raw dictionaries into instances of the configured Pydantic model
    for a specific metric, and serializes them into dictionaries for response.

    Args:
        metric_name (str): The identifier name of the metric.
        values (List[dict]): The raw data values to convert.

    Returns:
        List[dict]: A list of serialized model instances matching the metric's structure.

    Raises:
        HTTPException: If the metric_id is unsupported or misconfigured.
    """
    model = METRICS_CONFIG.get(metric_name, {}).get("model")
    if not model:
        raise UnsupportedMetricException(metric_name)

    return [model(**item).model_dump() for item in values]
