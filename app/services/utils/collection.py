from typing import Optional, Dict, Any
import requests
from app.utils import config
from app.utils.errors import raise_http_exception

settings = config.get_settings()


def get_collection_items_url(collection_id: str) -> Optional[str]:
    collection_url = f"{settings.stac_url}{collection_id}"
    try:
        response = requests.get(collection_url)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            raise_http_exception(404, "collection_not_found", collection_url)
        else:
            raise_http_exception(500, "http_error", collection_url)

    collection_data = response.json()
    if not collection_data:
        raise_http_exception(404, "no_features", collection_url)

    items_url = f"{collection_url}/items"
    try:
        response = requests.get(items_url)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            raise_http_exception(404, "items_not_found", items_url)
        else:
            raise_http_exception(500, "http_error", items_url)

    return items_url


def load_first_item_asset(items_url: str) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(items_url)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            raise_http_exception(404, "items_not_found", items_url)
        else:
            raise_http_exception(500, "http_error", items_url)

    items_data = response.json()
    if not items_data.get("features"):
        raise_http_exception(404, "no_features", items_url)

    first_item = items_data["features"][0]
    assets = first_item.get("assets", {})
    if not assets:
        raise_http_exception(404, "no_assets", items_url)

    first_asset = list(assets.values())[0]
    if not first_asset:
        raise_http_exception(404, "no_valid_asset", items_url)

    return first_asset


def get_first_item_asset_from_collection(
    collection_id: str,
) -> Optional[Dict[str, Any]]:
    items_url = get_collection_items_url(collection_id)
    first_asset = load_first_item_asset(items_url)

    value_href = first_asset.get("href")
    if not value_href:
        raise_http_exception(404, "no_href", items_url)

    return value_href
