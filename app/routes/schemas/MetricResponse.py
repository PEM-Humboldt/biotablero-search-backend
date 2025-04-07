from pydantic import BaseModel, Field
from typing import Union, List


class LossPersistenceResponse(BaseModel):
    perdida: float
    persistencia: float
    no_bosque: float
    periodo: str

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


# dict is temporal because of the type checking, remove after adding another type
MetricResponse = Union[LossPersistenceResponse, dict]


class LayerResponse(BaseModel):
    layer: str

    class Config:
        json_schema_extra = {
            "example": {
                "layer": "iVBORw0KGgoAAAANSUhEUgAAAKIAAAC4CAYAAABgvzfmAAABPElEQVR4nO3d2w6CMAwA0Gn8..."
            }
        }


class PolygonResponse(BaseModel):
    id: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 123456
            }
        }
