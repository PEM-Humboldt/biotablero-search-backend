from typing import List, Tuple, Dict

import requests
from pydantic import BaseModel

from app.models.models import Metric
from app.utils import config
from app.utils.errors import NotFoundError

settings = config.get_settings()


class MetadataProperties(BaseModel):
    values: List[int]
    colors: List[str]
    classes: List[str]


async def fetch_collection_metadata(
    metric_name: str,
) -> Tuple[Dict[str, int], List[int], List[str]]:

    metric_obj = await Metric.get_or_none(
        short_name=metric_name
    ).prefetch_related("collection")

    if not metric_obj:
        raise NotFoundError(
            usr_msg=f"There was an error retrieving metric data with name '{metric_name}'",
            log_msg=f"Metric not found: {metric_name}",
        )

    collection_obj = metric_obj.collection

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
            collection_obj.name,
        )

    except Exception as e:
        raise Exception(f"Error obtaining metadata: {str(e)}")
