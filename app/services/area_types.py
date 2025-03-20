from typing import List
from app.routes.schemas.AreaType import AreaType

def get_all() -> List[AreaType]:
    return [
        {
            "id": "id example",
            "label": "label example",
        }
    ]