from pydantic import BaseModel, Field, field_validator
from geojson_pydantic import Feature, geometries, types
from typing import Union

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
    bbox: types.BBox

    @field_validator("bbox", mode="before")
    def validate_bbox(cls, v):
        if len(v) not in [4, 6]:
            raise ValueError("Bounding box (bbox) must have 4 or 6 elements.")
        min_lon, min_lat, max_lon, max_lat = v[:4]
        if not (-180 <= min_lon <= 180) or not (-180 <= max_lon <= 180):
            raise ValueError("Longitude values must be between -180 and 180.")
        if not (-90 <= min_lat <= 90) or not (-90 <= max_lat <= 90):
            raise ValueError("Latitude values must be between -90 and 90.")
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


class PolygonFeature(Feature):
    geometry: Union[PolygonGeometry, None]


class Polygon(BaseModel):
    polygon: PolygonFeature = Field(
        description="GeoJSON polygon to determine the query area",
        example=geojson_polygon,
    )
