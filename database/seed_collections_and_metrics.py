from app.models.models import Collection, Metric
from datetime import datetime
from enum import Enum


STAC_BASE_URL = "http://172.191.168.255:8082"


class CollectionEnum(Enum):
    LOSS_PERSISTENCE = (
        1,
        "LossPersistence",
        "Loss and Persistence",
        f"{STAC_BASE_URL}/collections/LossPersistence",
    )
    COVERAGE = (
        2,
        "Coverage",
        "Coverage",
        f"{STAC_BASE_URL}/collections/Coverage",
    )
    HUMAN_FOOTPRINT = (
        3,
        "HumanFootprint",
        "Human Footprint",
        f"{STAC_BASE_URL}/collections/HumanFootprint",
    )

    def __init__(
        self, id_: int, short_name: str, display_name: str, stac_url: str
    ):
        self.id = id_
        self.short_name = short_name
        self.display_name = display_name
        self.stac_url = stac_url


async def seed_collections_and_metrics():
    if not await Collection.exists():
        now = datetime.now()
        collections = [
            Collection(
                id=col.id,
                name=col.short_name,
                stac_url=col.stac_url,
                updated_at=now,
            )
            for col in CollectionEnum
        ]
        await Collection.bulk_create(collections)

    if not await Metric.exists():
        metrics = [
            Metric(
                id=col.id,
                short_name=col.short_name,
                name=col.display_name,
                collection_id=col.id,
            )
            for col in CollectionEnum
        ]
        await Metric.bulk_create(metrics)
