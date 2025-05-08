import hashlib
import json

from app.routes.schemas.PolygonRequest import PolygonGeometry
from shapely.geometry import shape
from pyproj import Transformer
from shapely.ops import transform


def generate_hash(polygon: PolygonGeometry) -> str:
    """Generates a unique hash based on the geometry."""
    data = json.dumps(polygon.model_dump(), sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()


def get_polygon_area_ha(polygon: PolygonGeometry) -> float:
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
