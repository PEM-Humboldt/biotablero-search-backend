from typing import Optional

import requests

from typing import Dict, Any

from app.utils.config import get_settings

settings = get_settings()


def load_collection_items(url: str, collection_id: str) -> Optional[Dict[str, Any]]:
    response = requests.get(url)
    response.raise_for_status()
    collections_data = response.json()

    collection = next((col for col in collections_data.get('collections', []) if col['id'] == collection_id), None)
    print(collection)
    if collection:
        items = collection.get('items', [])
        if items:
            return items
    return None


