from typing import List, Tuple, Dict

import requests
from pydantic import BaseModel

from app.models.models import Collection
from app.utils import url, config

settings = config.get_settings()


class MetadataProperties(BaseModel):
    values: List[int]
    colors: List[str]
    classes: List[str]


async def fetch_collection_metadata(
    metric_name: str,
) -> Tuple[Dict[str, int], List[int], List[str]]:

    collection_obj = await Collection.get_or_none(name=metric_name)

    try:
        response = requests.get(collection_obj.stac_url)
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

        categories = {
            class_name: value
            for class_name, value in zip(
                metadata_properties.classes, metadata_properties.values
            )
        }

        return (
            categories,
            metadata_properties.values,
            metadata_properties.colors,
        )

    except Exception as e:
        raise Exception(f"Error obtaining metadata: {str(e)}")
