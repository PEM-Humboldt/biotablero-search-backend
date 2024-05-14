from pydantic import BaseModel, Field
from geojson_pydantic import Feature

coordinates = [
    [-78.990935, 12.437303],
    [-78.990935, 4.214931],
    [-66.851117, 4.214931],
    [-66.851117, 12.437303],
    [-78.990935, 12.437303],
]

geojson_polygon = {
    "type": "Feature",
    "properties": {},
    "geometry": {"type": "Polygon", "coordinates": [coordinates]},
}


class Polygon(BaseModel):
    polygon: Feature = Field(
        description="GeoJSON polygon to determine the query area",
        example=geojson_polygon,
    )
