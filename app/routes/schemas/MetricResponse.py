from typing import Union
from pydantic import BaseModel


class LossPersistenceResponse(BaseModel):
    """
    Response model for forest loss and persistence metrics in a given period.
    """

    periodo: str = ""
    perdida: float = 0
    persistencia: float = 0
    no_bosque: float = 0

    class Config:
        json_schema_extra = {
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
            ]
        }


class CoverageResponse(BaseModel):
    """
    Response model for land cover metrics in a given year.
    """

    ano: str = ""
    natural: float = 0
    secundaria: float = 0
    transformada: float = 0

    class Config:
        json_schema_extra = {
            "example": [
                {
                    "ano": "2021",
                    "natural": 1971.3859302816563,
                    "secundaria": 161349.158786824,
                    "transformada": 192519.67643274338,
                }
            ]
        }


MetricResponse = Union[LossPersistenceResponse, CoverageResponse]


class LayerResponse(BaseModel):
    layer: str

    class Config:
        json_schema_extra = {
            "example": {"layer_url": "http://localhost:4556/eads345.../layer"}
        }
