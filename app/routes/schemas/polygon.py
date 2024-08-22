from pydantic import BaseModel, Field, field_validator
from geojson_pydantic import Feature, geometries, types
from typing import Union, Tuple

from app.utils.errors import raise_http_exception

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
            raise_http_exception(422, "bbox_length", url="None")
        min_lon, min_lat, max_lon, max_lat = v[:4]
        if not (-180 <= min_lon <= 180) or not (-180 <= max_lon <= 180):
            raise_http_exception(422, "bbox_longitude", url="None")
        if not (-90 <= min_lat <= 90) or not (-90 <= max_lat <= 90):
            raise_http_exception(422, "bbox_latitude", url="None")
        if min_lon > max_lon:
            raise_http_exception(422, "bbox_min_max_longitude", url="None")
        if min_lat > max_lat:
            raise_http_exception(422, "bbox_min_max_latitude", url="None")
        if len(v) == 6:
            min_alt, max_alt = v[4], v[5]
            if min_alt > max_alt:
                raise_http_exception(422, "bbox_min_max_altitude", url="None")
        return v


class PolygonFeature(Feature):
    geometry: Union[PolygonGeometry, None]


class Polygon(BaseModel):
    polygon: PolygonFeature = Field(
        description="GeoJSON polygon to determine the query area",
        example=geojson_polygon,
    )
