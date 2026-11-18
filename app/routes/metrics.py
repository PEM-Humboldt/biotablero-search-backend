import fastapi

from typing import Annotated, cast
from fastapi import Path, Query

from app.middleware.exceptions import UnsupportedMetricException
from app.routes.schemas.LayerResponse import LayerResponse
from app.routes.schemas.MetricInfoResponse import MetricInfoListResponse
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
            description=(
                "Metric you wish to query. These are the available metrics; "
                "please note that not all metrics are available for all endpoints."
            ),
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
            description=(
                "Optional group identifier to filter results by. Use "
                "GET /metrics/{metric_id}/groups to see the groups available "
                "for a given metric. If the metric doesn't support groups, "
                "this parameter is silently ignored and the metric's "
                "regular (non-grouped) values are returned."
            ),
        ),
    ] = None,
) -> MetricResponse:
    """Returns serialized metric values for a given polygon ID and metric."""
    metric_id, metric_config = metric

    values = await metrics_service.get_or_create_polygon_metric(
        polygon_id, metric_id, group=group
    )
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
    group: Annotated[
        str | None,
        Query(
            description=(
                "Optional group identifier to filter the layer by. Use "
                "GET /metrics/{metric_id}/groups to see the groups available "
                "for a given metric. If the metric doesn't support groups, "
                "this parameter is silently ignored and the metric's "
                "regular (non-grouped) layer is returned."
            ),
        ),
    ] = None,
) -> LayerResponse:
    """
    Returns the url of rendered image layer for a given metric, polygon ID, item ID, and category,
    typically used to visualize spatial data such as forest loss, persistence, or non-forest areas.
    """

    metric_id, _ = metric
    layer = await metrics_service.get_or_create_polygon_metric_layer(
        metric_id, polygon_id, item_id, class_id, group=group
    )
    return LayerResponse(**layer)


@router.get(
    "/{metric_id}/info",
    response_model=MetricInfoListResponse,
    responses={
        200: {
            "description": "Metric information",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "type": "meto",
                            "description": "Descripción de la metodología de la métrica en HTML",
                        }
                    ]
                }
            },
        },
    },
)
async def get_metric_info(
    metric: Annotated[
        tuple[str, MetricConfig], fastapi.Depends(metric_id_param)
    ],
):
    """Returns the information associated with a given metric."""
    metric_id, _ = metric

    return await metrics_service.get_metric_info(metric_id)


@router.get(
    "/{metric_id}/groups",
    responses={
        200: {
            "description": "Group identifiers available to filter this metric",
            "content": {
                "application/json": {
                    "example": ["aves", "mamiferos", "reptiles"]
                }
            },
        }
    },
)
async def get_groups_by_metric(
    metric: Annotated[
        tuple[str, MetricConfig], fastapi.Depends(metric_id_param)
    ],
) -> list[str]:
    """Returns whether a metric's results can be filtered by group, and which groups are available."""
    metric_id, _ = metric
    return await metrics_service.get_metric_groups(metric_id)
