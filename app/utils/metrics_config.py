from typing import Any, Generic, List, Type, TypeVar, TypedDict

from app.routes.schemas.MetricResponse import (
    LossPersistenceResponse,
    CoverageResponse,
    CurrentHFResponse,
    CurrentHFAverageResponse,
    ParamoResponse,
    TropicalDryForestResponse,
    WetlandResponse,
)

T = TypeVar("T")


class MetricConfigBase(TypedDict, Generic[T]):
    model: Type[T]
    description: str
    example: Any


class MetricConfigList(MetricConfigBase[T]):
    example: List[T]


class MetricConfigSingle(MetricConfigBase[T]):
    example: T


class MetricsConfigType(TypedDict):
    lossPersistence: MetricConfigList[LossPersistenceResponse]
    coverage: MetricConfigSingle[CoverageResponse]
    currentHF: MetricConfigSingle[CurrentHFResponse]
    currentHF_average: MetricConfigSingle[CurrentHFAverageResponse]
    paramo: MetricConfigSingle[ParamoResponse]
    tropicalDryForest: MetricConfigSingle[TropicalDryForestResponse]
    wetland: MetricConfigSingle[WetlandResponse]


# This config contains everything related to FastAPI and Pydantic validations
# Anything related to processing logic must be stored in database
METRICS_CONFIG: MetricsConfigType = {
    "lossPersistence": {
        "model": LossPersistenceResponse,
        "example": [
            LossPersistenceResponse(
                Perdida=1971.3859302816563,
                Persistencia=161349.158786824,
                **{"No Bosque": 192519.67643274338},
                id="2016-2021",
            ),
            LossPersistenceResponse(
                Perdida=1572.6614325195167,
                Persistencia=162684.80917653913,
                **{"No Bosque": 191582.75054079038},
                id="2011-2015",
            ),
            LossPersistenceResponse(
                Perdida=844.3758017993621,
                Persistencia=164716.61720378936,
                **{"No Bosque": 190279.2281442603},
                id="2006-2010",
            ),
            LossPersistenceResponse(
                Perdida=1164.8889557696975,
                Persistencia=165904.73952933252,
                **{"No Bosque": 188770.59266474683},
                id="2000-2005",
            ),
        ],
        "description": "Forest loss and persistence",
    },
    "coverage": {
        "model": CoverageResponse,
        "example": CoverageResponse(
            id="2021",
            Natural=180000.0,
            Secundaria=25000.0,
            Transformada=12000.0,
        ),
        "description": "Land cover",
    },
    "currentHF": {
        "model": CurrentHFResponse,
        "example": CurrentHFResponse(
            id="2021",
            Natural=1971.38,
            Baja=161349.15,
            Media=192519.67,
            Alta=194312.67,
            **{"Muy Alta": 194312.67},
        ),
        "description": "Categorized human footprint index",
    },
    "currentHF_average": {
        "model": CurrentHFAverageResponse,
        "example": CurrentHFAverageResponse(
            id="2018",
            Average=12.34,
        ),
        "description": "Average human footprint index",
    },
    "paramo": {
        "model": ParamoResponse,
        "example": ParamoResponse(
            id="Paramos30",
            Paramo=25091,
        ),
        "description": "Paramo area",
    },
    "tropicalDryForest": {
        "model": TropicalDryForestResponse,
        "example": TropicalDryForestResponse(
            id="BosqueSeco30",
            BosqueSeco=1730,
        ),
        "description": "Tropical dry forest area",
    },
    "wetland": {
        "model": WetlandResponse,
        "example": WetlandResponse(
            id="Humedales30",
            Humedal=9287,
        ),
        "description": "Wetland area",
    },
    # "coverage_paramo": {},
    # "coverage_tropicalDryForest": {},
    # "coverage_wetland": {},
    # "timelineHF": {},
    # TODO: implementar estas:
    # "sciPersistenceHF": {},
    # "currentHF_average": {},
    # "protectedAreas": {},
    # "protectedAreas_paramo": {},
    # "protectedAreas_tropicalDryForest": {},
    # "protectedAreas_wetland": {},
    # "sciPersistenceHF_protectedAreas": {}
}

ALLOWED_METRICS = list(METRICS_CONFIG.keys())
ALLOWED_METRICS_DISPLAY = ", ".join(
    f"`{metric}`" for metric in ALLOWED_METRICS
)
