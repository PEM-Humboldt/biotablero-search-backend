from pydantic import BaseModel, Field, field_validator
from geojson_pydantic import Feature, geometries
from fastapi.exceptions import ValidationException

coordinates = [
    [-74.66791948382932, 3.9616641000901702],
    [-74.54883485657162, 3.6278270139496063],
    [-73.91938754106665, 3.8258815720871353],
    [-74.3787139604892, 4.312330649691575],
    [-74.66791948382932, 3.9616641000901702],
]

bbox = [
    -74.66791948382932,
    3.6278270139496063,
    -73.91938754106665,
    4.312330649691575,
]

geojson_polygon = {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Polygon",
        "bbox": bbox,
        "coordinates": [coordinates],
    },
}

error_template = {
    "type": "invalid_bbox",
    "loc": ("body", "polygon", "geometry", "bbox"),
    "msg": "",
}


class PolygonGeometry(geometries.Polygon):
    def __init__(self, **args):
        if "bbox" not in args:
            error_template["msg"] = (
                "bbox attribute in polygon geometry is required."
            )
            raise ValidationException([error_template])
        super().__init__(**args)

    @field_validator("bbox", mode="before")
    def validate_bbox(cls, bbox):

        if bbox is None:
            error_template["msg"] = (
                "Bounding box (bbox) is required and cannot be None."
            )
            raise ValidationException([error_template])

        if bbox is not None and len(bbox) not in [4, 6]:
            error_template["msg"] = (
                "Bounding box (bbox) must have 4 or 6 elements."
            )
            raise ValidationException([error_template])

        min_lon, min_lat, max_lon, max_lat = bbox[:4]
        if not (-180 <= min_lon <= 180) or not (-180 <= max_lon <= 180):
            error_template["msg"] = (
                "Longitude values must be between -180 and 180."
            )
            raise ValidationException([error_template])
        if not (-90 <= min_lat <= 90) or not (-90 <= max_lat <= 90):
            error_template["msg"] = (
                "Latitude values must be between -90 and 90."
            )
            raise ValidationException([error_template])
        if min_lon > max_lon:
            error_template["msg"] = (
                "Minimum longitude cannot be greater than maximum longitude."
            )
            raise ValidationException([error_template])
        if min_lat > max_lat:
            error_template["msg"] = (
                "Minimum latitude cannot be greater than maximum latitude."
            )
            raise ValidationException([error_template])
        if len(bbox) == 6:
            min_alt, max_alt = bbox[4], bbox[5]
            if min_alt > max_alt:
                error_template["msg"] = (
                    "Minimum altitude cannot be greater than maximum altitude."
                )
                raise ValidationException([error_template])


class PolygonFeature(Feature):
    geometry: PolygonGeometry


class PolygonRequest(BaseModel):
    polygon: PolygonFeature = Field(
        description="GeoJSON polygon to determine the query area",
    )

    class Config:
        json_schema_extra = {"example": {"polygon": geojson_polygon}}
