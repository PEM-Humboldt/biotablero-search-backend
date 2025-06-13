from typing import Union
from pydantic import BaseModel


class MetricResponseBase(BaseModel):
    """
    Base class for metric response models.
    """

    pass


class LossPersistenceResponse(MetricResponseBase):
    """
    Response model for forest loss and persistence metrics in a given period.
    """

    periodo: str = ""
    perdida: float = 0
    persistencia: float = 0
    no_bosque: float = 0

    class Config:
        json_schema_extra = {
            "example": {
                "periodo": "2016-2021",
                "perdida": 1971.3859302816563,
                "persistencia": 161349.158786824,
                "no_bosque": 192519.67643274338,
            }
        }


class CoverageResponse(MetricResponseBase):
    """
    Response model for land cover metrics in a given year.
    """

    ano: str = ""
    natural: float = 0
    secundaria: float = 0
    transformada: float = 0

    class Config:
        json_schema_extra = {
            "example": {
                "ano": "2021",
                "natural": 1971.3859302816563,
                "secundaria": 161349.158786824,
                "transformada": 192519.67643274338,
            }
        }


MetricResponse = Union[LossPersistenceResponse, CoverageResponse]


class LayerResponse(BaseModel):
    layer: str

    class Config:
        json_schema_extra = {
            "example": {"layer_url": "http://localhost:4556/eads345.../layer"}
        }
