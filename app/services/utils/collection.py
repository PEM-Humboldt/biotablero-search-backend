import typing
import requests
from app.utils import config
from app.utils.errors import raise_http_exception

settings = config.get_settings()



def get_collection_items_url(collection_id: str) -> str:
    collection_url = f"{settings.stac_url}/collections/{collection_id}"

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
            raise_http_exception(404, "items_not_found", items_url)
        else:
            raise_http_exception(500, "http_error", items_url)

    items_data = response.json()
    if not items_data.get("features"):
        raise_http_exception(404, "no_features", items_url)


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
