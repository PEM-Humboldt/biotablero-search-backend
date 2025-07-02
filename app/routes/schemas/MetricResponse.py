from typing import Dict, TypedDict, Type, List
from pydantic import BaseModel


class LossPersistenceResponse(BaseModel):
    """
    Response model for forest loss and persistence metrics in a given period.
    """

    periodo: str = ""
    perdida: float = 0
    persistencia: float = 0
    no_bosque: float = 0


class CoverageResponse(BaseModel):
    """
    Response model for land cover metrics in a given year.
    """

    ano: str = ""
    natural: float = 0
    secundaria: float = 0
    transformada: float = 0


class HumanTraceResponse(BaseModel):
    """
    Response model for Human Trace metrics in a given year.
    """

    ano: str = ""
    natural: float = 0
    baja: float = 0
    media: float = 0
    alta: float = 0


class MetricConfig(TypedDict):
    model: Type[BaseModel]
    example: List[dict]
    description: str
    group_key: str


METRICS_CONFIG: Dict[str, MetricConfig] = {
    "LossPersistence": {
        "model": LossPersistenceResponse,
        "example": [
            {
                "perdida": 1971.3859302816563,
                "persistencia": 161349.158786824,
                "no_bosque": 192519.67643274338,
                "periodo": "2016-2021",
            },
            {
                "perdida": 1572.6614325195167,
                "persistencia": 162684.80917653913,
                "no_bosque": 191582.75054079038,
                "periodo": "2011-2015",
            },
            {
                "perdida": 844.3758017993621,
                "persistencia": 164716.61720378936,
                "no_bosque": 190279.2281442603,
                "periodo": "2006-2010",
            },
            {
                "perdida": 1164.8889557696975,
                "persistencia": 165904.73952933252,
                "no_bosque": 188770.59266474683,
                "periodo": "2000-2005",
            },
        ],
        "description": "Forest loss and persistence",
        "group_key": "periodo",
    },
    "Coverage": {
        "model": CoverageResponse,
        "example": [
            {
                "ano": "2021",
                "natural": 180000.0,
                "secundaria": 25000.0,
                "transformada": 12000.0,
            }
        ],
        "description": "Land cover",
        "group_key": "ano",
    },
    "CurrentHF": {
        "model": HumanTraceResponse,
        "example": [
            {
                "ano": "2021",
                "natural": 1971.38,
                "baja": 161349.15,
                "media": 192519.67,
                "alta": 194312.67,
            }
        ],
        "description": "Human footprint",
        "group_key": "ano",
    },
}
