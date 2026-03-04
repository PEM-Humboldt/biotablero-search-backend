from pyexpat import features
from typing import List, Tuple, Dict
from pydantic import BaseModel
import requests

from app.models.models import Collection

from app.utils.errors import ServerError, NotFoundError
from app.utils import config, url

settings = config.get_settings()


class MetadataProperties(BaseModel):
    values: List[int]
    colors: List[str]
    classes: List[str]


async def fetch_collection_metadata(
    collection: Collection,
) -> Tuple[Dict[str, int], List[int], List[str]]:
    try:
        collection_url = url.build_url(
            settings.stac_url, f"/collections/{collection.name}"
        )
        response = requests.get(collection_url)
        response.raise_for_status()
        collection_metadata = response.json()

        if (
            "metadata" not in collection_metadata
            or "properties" not in collection_metadata["metadata"]
        ):
            raise ValueError(
                "The 'metadata' or 'properties' key is not found in the response."
            )

        properties = collection_metadata["metadata"]["properties"]
        metadata_properties = MetadataProperties(
            values=properties.get("values", []),
            colors=properties.get("colors", []),
            classes=properties.get("classes", []),
        )

        classes_map = {
            class_name: value
            for class_name, value in zip(
                metadata_properties.classes, metadata_properties.values
            )
        }

        return (
            classes_map,
            metadata_properties.values,
            metadata_properties.colors,
        )

    except Exception as e:
        raise Exception(f"Error obtaining metadata: {str(e)}")


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
) -> List[tuple[str, str]]:
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

    assets_urls: List[tuple[str, str | None]] = list(
        map(
            lambda item: (item["id"], get_asset_url(item)),
            items_data.get("features"),
        )
    )

    return [(id, url) for id, url in assets_urls if url is not None]


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


def get_item_resolution(collection_id: str, index_item: int) -> float:
    """
    Returns the spatial resolution of the item at the given index in the collection.
    """
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

    if index_item < 0 or index_item >= len(items_data["features"]):
        raise NotFoundError(
            usr_msg="Requested item index is out of range",
            log_msg=(
                f"Index {index_item} out of range for collection "
                f"{collection_id}. Items available: {len(features)}"
            ),
        )
    item = items_data.get("features")[index_item]
    for asset in item.get("assets", {}).values():
        for band in asset.get("raster:bands", []):
            if "spatial_resolution" in band:
                resolution = band["spatial_resolution"]
                return resolution

    raise NotFoundError(
        usr_msg="Item has no spatial resolution information",
        log_msg=f"Item {index_item} in collection {collection_id} has no raster bands with spatial_resolution",
    )


def get_item_index_by_resolution(collection_id: str, resol_obj: float) -> int:
    """
    Returns the index of the item in the collection that has the closest spatial resolution to the given value.
    """
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

    items = items_data.get("features", {})
    item_resolutions: list[tuple[int, float]] = []

    for idx, item in enumerate(items):
        for asset in item.get("assets", {}).values():
            for band in asset.get("raster:bands", []):
                resolution = band.get("spatial_resolution")
                if resolution is not None:
                    item_resolutions.append((idx, resolution))
                    break
            if resolution is not None:
                break
    if not item_resolutions:
        raise NotFoundError(
            usr_msg="No spatial resolution information found in any item",
            log_msg=f"No raster bands with spatial_resolution found in collection {collection_id}",
        )

    closest_item_index, _ = min(
        item_resolutions,
        key=lambda x: abs(x[1] - resol_obj),
    )
    return closest_item_index
