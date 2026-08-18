import fastapi

from typing import Annotated, cast
from fastapi import Path, Query

from app.middleware.exceptions import UnsupportedMetricException
from app.routes.schemas.LayerResponse import LayerResponse
from app.utils.metrics_config import (
    ALLOWED_METRICS,
    METRICS_CONFIG,
    MetricConfig,
    MetricResponse,
)
import app.services.metrics as metrics_service

validation_error_example = {
    "detail": [
        {
            "loc": ["body", "polygon"],
            "msg": "Field required",
            "type": "value_error.missing",
        }
    ]
}

router = fastapi.APIRouter(
    prefix="/metrics",
    tags=["metrics"],
    responses={
        400: {
            "description": "Bad request. Possibly due to an unsupported metric_id.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Unsupported metric. Allowed values: LossPersistence, Coverage, CurrentHF, Paramo, TropicalDryForest, Wetland"
                    }
                }
            },
        },
        404: {"description": "Not found"},
        422: {
            "description": "Validation or unprocessable error",
            "content": {
                "application/json": {"example": validation_error_example}
            },
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "message": "An internal server error occurred."
                    }
                }
            },
        },
    },
)


async def metric_id_param(
    metric_id: Annotated[
        str,
        Path(
            description=f"Metric you wish to query. See the examples list",
            examples=ALLOWED_METRICS,
        ),
    ],
) -> tuple[str, MetricConfig]:
    if metric_id not in METRICS_CONFIG:
        raise UnsupportedMetricException(metric_id)
    return (metric_id, METRICS_CONFIG[metric_id])


def build_documentation_examples():
    result = {}

    for metric_key, v in METRICS_CONFIG.items():
        config = cast(MetricConfig, v)

        result[metric_key] = {
            "summary": metric_key,
            "value": config["example"],
            "description": config["description"],
        }

    return result


@router.get(
    "/{metric_id}/values/{polygon_id}",
    responses={
        200: {
            "description": "Metric data by polygon",
            "content": {
                "application/json": {
                    "examples": build_documentation_examples()
                }
            },
        }
    },
)
async def get_values_by_polygon(
    metric: Annotated[
        tuple[str, MetricConfig], fastapi.Depends(metric_id_param)
    ],
    polygon_id: int,
    group: Annotated[
        str | None,
        Query(
            description="Optional species group slug to filter species stats",
        ),
    ] = None,
) -> MetricResponse:
    """Returns serialized metric values for a given polygon ID and metric."""
    metric_id, metric_config = metric

    values = await metrics_service.get_or_create_polygon_metric(
        polygon_id, metric_id, group=group
    )

    response_parser = metric_config.get("response_parser")
    if response_parser is not None:
        return response_parser(values, group)

    model_response = metric_config["model"]
    return model_response.model_validate(values, by_alias=True)


@router.get(
    "/{metric_id}/layer",
    response_model=LayerResponse,
    responses={
        200: {
            "description": "Rendered image layer URL",
            "content": {
                "application/json": {
                    "example": {
                        "layer": "http://localhost:4556/layer/preview.png"
                    }
                }
            },
        }
    },
)
async def get_layer_by_polygon(
    metric: Annotated[
        tuple[str, MetricConfig], fastapi.Depends(metric_id_param)
    ],
    polygon_id: Annotated[int, Query(description="Polygon ID to use")],
    item_id: Annotated[
        str,
        Query(
            description="The ID of the item, corresponds to the id of a values object",
            examples=["2016-2021"],
        ),
    ],
    class_id: Annotated[
        str,
        Query(
            description=(
                "Class value associated to the layer requested, corresponds to one of the keys in a values object (except 'id') "
                "For example: Natural"
                "For metrics based on continous collections (e.g. recordGaps, richness), "
                "class_id must be the metric's own name instead of a class key"
            ),
            examples=["Natural"],
        ),
    ],
) -> LayerResponse:
    """
    Returns the url of rendered image layer for a given metric, polygon ID, item ID, and category,
    typically used to visualize spatial data such as forest loss, persistence, or non-forest areas.
    """

    metric_id, _ = metric
    layer = await metrics_service.get_or_create_polygon_metric_layer(
        metric_id, polygon_id, item_id, class_id
    )
    return LayerResponse(**layer)
