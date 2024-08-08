from typing import Optional, Dict, Any

import requests


def find_collection_url(base_url: str, collection_id: str) -> Optional[str]:
    response = requests.get(base_url)
    response.raise_for_status()
    root_data = response.json()

    for link in root_data.get("links", []):
        if link["rel"] == "child" and collection_id in link["href"]:
            return link["href"]

    return None


def get_collection_items_url(collection_url: str) -> Optional[str]:
    response = requests.get(collection_url)
    response.raise_for_status()
    collection_data = response.json()

    for link in collection_data.get("links", []):
        if link["rel"] == "items":
            return link["href"]

    return None


def load_first_item_asset(items_url: str) -> Optional[Dict[str, Any]]:
    response = requests.get(items_url)
    response.raise_for_status()
    items_data = response.json()

    if items_data.get("features"):
        first_item = items_data["features"][0]
        assets = first_item.get("assets", {})
        if assets:
            return list(assets.values())[0]

    return None
