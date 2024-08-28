from pydantic import BaseModel, Field, field_validator
from geojson_pydantic import Feature, geometries
from app.middleware.exceptions import BBoxValidationError

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


class PolygonGeometry(geometries.Polygon):
    def __init__(self, **args):
        if "bbox" not in args:
            raise BBoxValidationError(
                [], "bbox attribute in polygon geometry is required."
            )
        super().__init__(**args)

    @field_validator("bbox", mode="before")
    def validate_bbox(bbox: list):
        if len(bbox) not in [4, 6]:
            raise BBoxValidationError(
                bbox, "Bounding box (bbox) must have 4 or 6 elements."
            )

        min_lon, min_lat, max_lon, max_lat = bbox[:4]
        if not (-180 <= min_lon <= 180) or not (-180 <= max_lon <= 180):
            raise BBoxValidationError(
                bbox, "Longitude values must be between -180 and 180."
            )
        if not (-90 <= min_lat <= 90) or not (-90 <= max_lat <= 90):
            raise BBoxValidationError(
                bbox, "Latitude values must be between -90 and 90."
            )
        if min_lon > max_lon:
            raise BBoxValidationError(
                bbox,
                "Minimum longitude cannot be greater than maximum longitude.",
            )
        if min_lat > max_lat:
            raise BBoxValidationError(
                bbox,
                "Minimum latitude cannot be greater than maximum latitude.",
            )
        if len(bbox) == 6:
            min_alt, max_alt = bbox[4], bbox[5]
            if min_alt > max_alt:
                raise BBoxValidationError(
                    bbox,
                    "Minimum altitude cannot be greater than maximum altitude.",
                )


class PolygonFeature(Feature):
    geometry: PolygonGeometry


class Polygon(BaseModel):
    polygon: PolygonFeature = Field(
        description="GeoJSON polygon to determine the query area",
        examples=[geojson_polygon],
    )
