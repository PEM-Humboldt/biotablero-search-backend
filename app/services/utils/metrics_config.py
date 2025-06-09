from typing import Optional

from app.routes.schemas.MetricResponse import CoverageResponse, LossPersistenceResponse, MetricResponse


def metric_group_key(metric_id: str) -> Optional[str]:
    """
    For every known metric return the name of the key used to group categories
    """
    if metric_id == "LossPersistence":
        return "periodo"
    if metric_id == "Coverage":
        return "id"

    return None


def metric_response_type(metric_id: str) -> Optional[MetricResponse]:
    """
    Return MetricResponse type by metric id
    """
    if metric_id == "LossPersistence":
        return LossPersistenceResponse()
    if metric_id == "Coverage":
        return CoverageResponse()

    return None