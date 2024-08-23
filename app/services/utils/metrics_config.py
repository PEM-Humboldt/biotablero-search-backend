from typing import Optional, Dict, Any


def value_category_config(metric_id: str) -> Optional[Dict[Any, Any]]:
    """
    For every known metric return the map of category-value for their raster
    """
    if metric_id == "LossPersistence":
        return {"perdida": 0, "persistencia": 1, "no_bosque": 2}
    return None


def metric_group_key(metric_id: str) -> Optional[str]:
    """
    For every known metric return the name of the key used to group categories
    """
    if metric_id == "LossPersistence":
        return "periodo"
    return None
