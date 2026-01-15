import hashlib
import json
from typing import Any

from shapely.geometry import shape
from pyproj import Transformer
from shapely.ops import transform
from geojson_pydantic import MultiPolygon, Polygon as PydanticPolygon


def generate_hash(polygon: PydanticPolygon | MultiPolygon) -> str:
    """Generates a unique hash based on the geometry."""
    data = json.dumps(polygon.model_dump(), sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()


def get_polygon_area_ha(polygon: MultiPolygon) -> float:
    """
    Calculate polygon area in hectares, using projection EPSG:9377.
    """
    if polygon is None:
        raise ValueError("Polygon cannot be None")

    shapely_geom = shape(polygon)

    if shapely_geom.is_empty:
        raise ValueError("Geometry is empty.")

    transformer = Transformer.from_crs(
        "EPSG:4326", "EPSG:9377", always_xy=True
    )
    projected_geom = transform(transformer.transform, shapely_geom)

    area_ha = projected_geom.area / 10000
    return area_ha


def cast_to_multi_polygon(geometry: dict[str, Any]) -> dict[str, Any]:
    """
    Ensures that the geometry in the given object is a MultiPolygon.

    Parameters:
        polygon_obj: An object with a 'geometry' attribute containing a GeoJSON-like dict.

    Returns:
        The same object, with geometry cast to MultiPolygon if it was a Polygon.
    """
    geometry_type = geometry["type"]

    if geometry_type == "MultiPolygon":
        return geometry

    if geometry_type == "Polygon":
        polygon_bbox = geometry["bbox"]
        polygon = PydanticPolygon.model_validate(geometry)
        multi_polygon = MultiPolygon(
            type="MultiPolygon", coordinates=[polygon.coordinates]
        )
        multi_polygon_geometry = multi_polygon.model_dump()
        multi_polygon_geometry["bbox"] = polygon_bbox

        return multi_polygon_geometry

    raise ValueError(f"Invalid geometry type: {geometry_type}")
