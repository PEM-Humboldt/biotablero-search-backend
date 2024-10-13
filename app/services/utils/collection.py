import typing
import requests

from app.utils.errors import ServerError, NotFoundError
from app.utils import config, url

settings = config.get_settings()


def get_collection_items_url(collection_id: str) -> str:
    collection_url = url.build_url(
        settings.stac_url, f"/collections/{collection_id}"
    )
    response = None

    try:
        response = requests.get(collection_url)
        response.raise_for_status()
    except Exception as e:
        if response is not None and response.status_code == 404:
            raise NotFoundError(
                usr_msg=f"{collection_id} data not found",
                log_msg=f"Collection not found at URL: {collection_url}",
                e=e,
            )
        else:
            raise ServerError(
                code=500,
                usr_msg=f"There was an error retrieving {collection_id} data",
                e=e,
            )

    collection_data = response.json()
    if not collection_data:
        raise NotFoundError(
            usr_msg=f"{collection_id} data not found",
            log_msg=f"Collection was found but it was empty, collection url: {collection_url}",
        )

    return f"{collection_url}/items"


def get_items_asset_url(
    collection_id: str,
) -> typing.Dict[str, typing.Any]:
    items_url = get_collection_items_url(collection_id)
    response = None

    try:
        response = requests.get(items_url)
        response.raise_for_status()
    except Exception as e:
        if response is not None and response.status_code == 404:
            raise NotFoundError(
                usr_msg=f"{collection_id} data is incomplete",
                log_msg=f"Collection items not found at URL: {items_url}",
                e=e,
            )
        else:
            raise ServerError(
                code=500,
                usr_msg=f"There was an error retrieving {collection_id} data",
                e=e,
            )

    items_data = response.json()
    if not items_data.get("features"):
        raise NotFoundError(
            usr_msg=f"{collection_id} data is incomplete",
            log_msg=f"Collection items url exist but it has no features, url: {items_url}",
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


def get_asset_href_by_item_id(collection_id: str, item_id: str) -> str:
    item_id_url = url.build_url(
        settings.stac_url, f"/collections/{collection_id}/items/{item_id}"
    )
    response = None

    try:
        response = requests.get(item_id_url)
        response.raise_for_status()
    except Exception as e:
        if response is not None and response.status_code == 404:
            raise NotFoundError(
                usr_msg=f"item {item_id} not found in {collection_id}",
                log_msg=f"{item_id_url} not found",
                e=e,
            )
        else:
            raise ServerError(
                code=500,
                usr_msg=f"There was an error retrieving {collection_id} data",
                e=e,
            )

    item_data = response.json()
    asset_href = item_data.get("assets", {}).get(item_id, {}).get("href")
    if not asset_href:
        raise NotFoundError(
            usr_msg=f"item {item_id} asset not found",
            log_msg=f"assset not found item: {item_id_url}",
        )

    return asset_href
