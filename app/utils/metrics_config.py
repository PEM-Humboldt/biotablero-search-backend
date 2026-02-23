from typing import List, Dict

from app.middleware.exceptions import UnsupportedMetricException
from app.routes.schemas.MetricResponse import (
    MetricConfig,
    LossPersistenceResponse,
    CoverageResponse,
    CurrentHFResponse,
    CurrentHFAverageResponse,
)

# This config contains everything related to FastAPI and Pydantic validations
# Anything related to processing logic must be stored in database
METRICS_CONFIG: Dict[str, MetricConfig] = {
    "lossPersistence": {
        "model": LossPersistenceResponse,
        "example": [
            {
                "perdida": 1971.3859302816563,
                "persistencia": 161349.158786824,
                "no_bosque": 192519.67643274338,
                "id": "2016-2021",
            },
            {
                "perdida": 1572.6614325195167,
                "persistencia": 162684.80917653913,
                "no_bosque": 191582.75054079038,
                "id": "2011-2015",
            },
            {
                "perdida": 844.3758017993621,
                "persistencia": 164716.61720378936,
                "no_bosque": 190279.2281442603,
                "id": "2006-2010",
            },
            {
                "perdida": 1164.8889557696975,
                "persistencia": 165904.73952933252,
                "no_bosque": 188770.59266474683,
                "id": "2000-2005",
            },
        ],
        "description": "Forest loss and persistence",
    },
    "coverage": {
        "model": CoverageResponse,
        "example": {
            "id": "2021",
            "natural": 180000.0,
            "secundaria": 25000.0,
            "transformada": 12000.0,
        },
        "description": "Land cover",
    },
    "currentHF": {
        "model": CurrentHFResponse,
        "example": {
            "id": "2021",
            "natural": 1971.38,
            "baja": 161349.15,
            "media": 192519.67,
            "alta": 194312.67,
        },
        "description": "Categorized human footprint index",
    },
    "currentHF_average": {
        "model": CurrentHFAverageResponse,
        "example": {
            "id": "2018",
            "average": 12.34,
        },
        "description": "Average human footprint index",
    },
    # "coverage_paramo": {},
    # "coverage_tropicalDryForest": {},
    # "coverage_wetland": {},
    # "timelineHF": {},
    # TODO: implementar estas:
    # "paramo": {},
    # "tropicalDryForest": {},
    # "persistenceHF": {},
    # "sciPersistenceHF": {},
    # "currentHF_average": {},
    # "protectedAreas": {},
    # "protectedAreas_paramo": {},
    # "protectedAreas_tropicalDryForest": {},
    # "protectedAreas_wetland": {},
    # "sciPersistenceHF_protectedAreas": {}
}
