<<<<<<< Updated upstream
from pydantic import BaseModel, Field, field_validator
from geojson_pydantic import Feature
from typing import List, Optional
=======
from pydantic import BaseModel, Field
from geojson_pydantic.geometries import Polygon
>>>>>>> Stashed changes

from app.services.utils import context_vars


<<<<<<< Updated upstream
class PolygonRequest(BaseModel):
    type: str
    coordinates: List[List[List[float]]]
    bbox: Optional[List[float]] = None

    @field_validator("bbox")
    def validate_bbox(cls, v):
        if v is not None:
            if len(v) not in [4, 6]:
                raise ValueError(
                    "Bounding box (bbox) must have 4 o 6 elements."
                )
            min_lon, min_lat, max_lon, max_lat = v[:4]
            if not (-180 <= min_lon <= 180) or not (-180 <= max_lon <= 180):
                raise ValueError(
                    "Longitude values must be between -180 and 180."
                )
            if not (-90 <= min_lat <= 90) or not (-90 <= max_lat <= 90):
                raise ValueError("Latitude values must be between -90 y 90.")
            if min_lon > max_lon:
                raise ValueError(
                    "Minimum longitude cannot be greater than maximum longitude."
                )
            if min_lat > max_lat:
                raise ValueError(
                    "Minimum latitude cannot be greater than maximum latitude."
                )
            if len(v) == 6:
                min_alt, max_alt = v[4], v[5]
                if min_alt > max_alt:
                    raise ValueError(
                        "Minimum altitude cannot be greater than maximum altitude."
                    )
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [102.0, 2.0],
                        [103.0, 2.0],
                        [103.0, 3.0],
                        [102.0, 3.0],
                        [102.0, 2.0],
                    ]
                ],
                "bbox": [102.0, 2.0, 103.0, 3.0],
            }
        }


class FeatureRequest(BaseModel):
    type: str
    properties: dict
    geometry: PolygonRequest

    class Config:
        json_schema_extra = {
            "example": {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [102.0, 2.0],
                            [103.0, 2.0],
                            [103.0, 3.0],
                            [102.0, 3.0],
                            [102.0, 2.0],
                        ]
                    ],
                    "bbox": [102.0, 2.0, 103.0, 3.0],
                },
            }
        }


class WrappedFeatureRequest(BaseModel):
    polygon: FeatureRequest

    class Config:
        json_schema_extra = {
            "example": {
                "polygon": {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "Polygon",
                        "bbox": [
                            -76.2114265687811,
                            4.66464238363919,
                            -75.3755113620596,
                        ],
                        "coordinates": [
                            [
                                [-76.008254260126, 5.56368303184647],
                                [-76.0024992672274, 5.56019970305395],
                                [-76.0022908115716, 5.55269347472411],
                                [-75.9989734130925, 5.54151494575816],
                            ]
                        ],
                    },
                }
            }
        }
=======
class FeatureWithPolygon(BaseModel):
    type: str
    properties: dict
    geometry: Polygon = Field(
        description="GeoJSON polygon to determine the query area",
        example=geojson_polygon,
    )
>>>>>>> Stashed changes
