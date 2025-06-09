from pydantic import BaseModel


class MetricResponseBase(BaseModel):

    class Config:
        json_schema_extra = {
            "example": {
                "perdida": 1971.3859302816563,
                "persistencia": 161349.158786824,
                "no_bosque": 192519.67643274338,
                "periodo": "2016-2021",
            }
        }


class LossPersistenceResponse(MetricResponseBase):
    periodo: str = ""
    perdida: float = 0
    persistencia: float = 0
    no_bosque: float = 0


class CoverageResponse(MetricResponseBase):
    id: str = ""
    natural: float = 0
    secundaria: float = 0
    transformada: float = 0


MetricResponse = MetricResponseBase


class LayerResponse(BaseModel):
    layer: str

    class Config:
        json_schema_extra = {
            "example": {"layer_url": "http://localhost:4556/eads345.../layer"}
        }
