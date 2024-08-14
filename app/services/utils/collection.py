from typing import Optional, Dict, Any
import requests
from fastapi import HTTPException

from app.utils import config

settings = config.get_settings()


def get_collection_items_url(collection_id: str) -> Optional[str]:
    response = None
    collection_url = f"{settings.stac_url}{collection_id}"

    try:
        response = requests.get(collection_url)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"Collection not found at URL: {collection_url}",
            )
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"HTTP error occurred while accessing {collection_url}",
            )

    collection_data = response.json()

    if not collection_data:
        raise HTTPException(
            status_code=404,
            detail=f"No collection data found at URL: {collection_url}",
        )

    items_url = f"{collection_url}/items"

    try:
        response = requests.get(items_url)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            raise HTTPException(
                status_code=404, detail=f"Items not found at URL: {items_url}"
            )
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"HTTP error occurred while accessing {items_url}",
            )

    return items_url


def load_first_item_asset(items_url: str) -> Optional[Dict[str, Any]]:
    response = None
    try:
        response = requests.get(items_url)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            raise HTTPException(
                status_code=404, detail=f"Items not found at URL: {items_url}"
            )
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"HTTP error occurred while accessing {items_url}",
            )

    items_data = response.json()

    if not items_data.get("features"):
        raise HTTPException(
            status_code=404,
            detail=f"No features found in the items data at URL: {items_url}",
        )

    first_item = items_data["features"][0]
    assets = first_item.get("assets", {})

    if not assets:
        raise HTTPException(
            status_code=404,
            detail=f"No assets found in the first item at URL: {items_url}",
        )

    first_asset = list(assets.values())[0]

    if not first_asset:
        raise HTTPException(
            status_code=404,
            detail=f"No valid asset found in the first item at URL: {items_url}",
        )

    return first_asset


def get_first_item_asset_from_collection(
    collection_id: str,
) -> Optional[Dict[str, Any]]:
    items_url = get_collection_items_url(collection_id)

    first_asset = load_first_item_asset(items_url)

    value_href = first_asset.get("href")

    if not value_href:
        raise HTTPException(
            status_code=404, detail="No 'href' found in the first asset."
        )

    return value_href
