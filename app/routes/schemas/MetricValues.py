from pydantic import BaseModel, Field
from typing import Union


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
                "layer": "iVBORw0KGgoAAAANSUhEUgAAAKIAAAC4CAYAAABgvzfmAAABPElEQVR4nO3d2w6CMAwA0Gn8/1+er4pMLtko0HNeNIEso61Vh2ApAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAtBo9gYt7Rk8A6EQ3BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAyM3/2gEAAAAAANyFMz+EU4TjPKMnAAAAAPdlSQMAAABgpEePQaZLOF0GJZXdNdNaP1SE7LH7Z2AKjp5ePQZRlNxWLU4fAgAAAAAAAAAAAAAAAABcmMtFAaLowBckYRxt8SZMipIjNAtRAXIKPlMRqjaeQxhdcZ6YnET2RGQ//hFmv6wINKFq8Xa8RGx+1cnj2v1X7Zg14NMXY9Y4jPAvll/3Ya+tDUmJR1+1bIxj5o74SQyCZU1A1uM+rS0JkTwAnRAAAAAAAAAAAAAAAAA4szd/kzPnbncgtwAAAABJRU5ErkJggg=="
            }
        }
