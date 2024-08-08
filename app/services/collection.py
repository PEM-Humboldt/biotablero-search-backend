from typing import Optional, Dict, Any

import requests


def find_collection_url(base_url: str, collection_id: str) -> Optional[str]:
    response = requests.get(base_url)
    response.raise_for_status()
    root_data = response.json()

    for link in root_data.get("links", []):
        href = link.get("href")
        if (
            isinstance(href, str)
            and link.get("rel") == "child"
            and collection_id in href
        ):
            return href

    return None


def get_collection_items_url(collection_url: str) -> Optional[str]:
    response = requests.get(collection_url)
    response.raise_for_status()
    collection_data = response.json()

    for link in collection_data.get("links", []):
        if link.get("rel") == "items":
            return link.get("href")

    return None


def load_first_item_asset(items_url: str) -> Optional[Dict[str, Any]]:
    response = requests.get(items_url)
    response.raise_for_status()
    items_data = response.json()

    features = items_data.get("features")
    if isinstance(features, list) and features:
        first_item = features[0]
        assets = first_item.get("assets", {})
        if assets and isinstance(assets, dict):
            return next(iter(assets.values()), None)

    return None
