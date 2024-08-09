from typing import Optional, Dict, Any

import requests


def get_collection_items_url(
    base_url: str, collection_id: str
) -> Optional[str]:
    url = base_url + collection_id
    response = requests.get(url)
    response.raise_for_status()
    collection_data = response.json()

    items_url = None
    for link in collection_data.get("links", []):
        if link.get("rel") == "items":
            items_url = link["href"]
            break

    if not items_url:
        raise ValueError(
            f"No items URL found for collection at URL: {url}/items"
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


def get_first_item_asset_from_collection(
    base_url: str, collection_id: str
) -> Optional[Dict[str, Any]]:
    items_url = get_collection_items_url(base_url, collection_id)

    first_asset = load_first_item_asset(items_url)
    value_href = first_asset.get("href")

    if not value_href:
        raise ValueError("No 'href' found in the first asset.")
    return value_href
