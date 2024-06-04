from pydantic import BaseModel, Field
from geojson_pydantic import Feature

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


class Polygon(BaseModel):
    polygon: Feature = Field(
        description="GeoJSON polygon to determine the query area",
        example=geojson_polygon,
    )
