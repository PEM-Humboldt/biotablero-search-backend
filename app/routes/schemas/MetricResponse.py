from pydantic import BaseModel


class LossPersistenceResponse(BaseModel):
    perdida: float
    persistencia: float
    no_bosque: float
    periodo: str

    class Config:
        json_schema_extra = {
            "example": {
                "perdida": 1971.3859302816563,
                "persistencia": 161349.158786824,
                "no_bosque": 192519.67643274338,
                "periodo": "2016-2021",
            }
        }


MetricResponse = LossPersistenceResponse


class LayerResponse(BaseModel):
    layer: str

    class Config:
        json_schema_extra = {
            "example": {"layer_url": "http://localhost:4556/eads345.../layer"}
        }
