from typing import List

from fastapi import HTTPException

from app.routes.schemas.MetricResponse import METRICS_CONFIG


def metric_group_key(metric_id: str) -> str:
    group_key = METRICS_CONFIG.get(metric_id, {}).get("group_key")
    if group_key is None:
        raise ValueError(f"No group_key defined for metric_id '{metric_id}'")
    return group_key



def build_metric_response(metric_id: str, values: List[dict]) -> List[dict]:
    model = METRICS_CONFIG.get(metric_id, {}).get("model")
    if not model:
        raise HTTPException(status_code=400, detail="Unsupported metric")
    return [model(**item).model_dump() for item in values]
