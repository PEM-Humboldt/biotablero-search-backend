import typing
import requests
from fastapi import HTTPException

from app.utils import config

settings = config.get_settings()


def get_collection_items_url(collection_id: str) -> str:
    collection_url = f"{settings.stac_url}/collections/{collection_id}"

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

    return f"{collection_url}/items"


def get_items_asset_url(
    collection_id: str,
) -> typing.Dict[str, typing.Any]:
    items_url = get_collection_items_url(collection_id)

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

    def get_asset_url(item):
        assets = item.get("assets", {})
        if not assets:
            return None
        primary_asset = assets.get(item["id"])
        if not primary_asset:
            primary_asset = list(assets.values())[0]
        asset_url = primary_asset.get("href")
        return asset_url

    assets_urls = dict(
        map(
            lambda item: (item["id"], get_asset_url(item)),
            items_data.get("features"),
        )
    )

    return {k: v for k, v in assets_urls.items() if v is not None}
