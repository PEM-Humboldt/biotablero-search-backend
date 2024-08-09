from typing import Optional, Dict, Any

import requests


def find_collection_url(base_url: str, collection_id: str) -> Optional[str]:
    response = requests.get(base_url)
    response.raise_for_status()
    root_data = response.json()

    collection_url = None
    for link in root_data.get("links", []):
        href = link.get("href")
        if (
            isinstance(href, str)
            and link.get("rel") == "child"
            and collection_id in href
        ):
            collection_url = href
            break

    if not collection_url:
        raise ValueError(
            f"No collection found for id at URL: {base_url}/collections/{collection_id}"
        )

    return collection_url


def get_collection_items_url(collection_url: str) -> Optional[str]:
    response = requests.get(collection_url)
    response.raise_for_status()
    collection_data = response.json()

    items_url = None
    for link in collection_data.get("links", []):
        if link.get("rel") == "items":
            items_url = link["href"]
            break

    if not items_url:
        raise ValueError(
            f"No items URL found for collection at URL: {collection_url}/items"
        )

    return items_url


def load_first_item_asset(items_url: str) -> Optional[Dict[str, Any]]:
    response = requests.get(items_url)
    response.raise_for_status()
    items_data = response.json()

    first_asset = None
    if items_data.get("features"):
        first_item = items_data["features"][0]
        assets = first_item.get("assets", {})
        if assets:
            first_asset = list(assets.values())[0]

    if not first_asset:
        raise ValueError(f"No valid asset found at items URL: {items_url}")

    return first_asset
