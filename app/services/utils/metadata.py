from typing import List, Tuple, Dict

import requests
from pydantic import BaseModel


from app.utils import url, config

settings = config.get_settings()


class MetadataProperties(BaseModel):
    values: List[int]
    colors: List[str]
    classes: List[str]


def fetch_collection_metadata(
    metric_id: str,
) -> Tuple[Dict[str, int], List[int], List[str]]:
    collection_url = url.build_url(
        settings.stac_url, f"/collections/{metric_id}"
    )

    try:
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
