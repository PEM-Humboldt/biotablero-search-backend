from typing import Optional, Dict, Any


def metric_group_key(metric_id: str) -> Optional[str]:
    """
    For every known metric return the name of the key used to group categories
    """
    if metric_id == "LossPersistence":
        return "periodo"
    return None
