from tortoise import fields
from tortoise.models import Model

class SpatialRefSys(Model):
    srid = fields.IntField(pk=True)
    auth_name = fields.CharField(max_length=256, null=True)
    auth_srid = fields.IntField(null=True)
    srtext = fields.TextField(null=True)
    proj4text = fields.TextField(null=True)


class Polygons(Model):
    polygon_id = fields.IntField(pk=True)
    polygon_geometry = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True)



class MetricPolygons(Model):
    metric_polygon_id = fields.IntField(pk=True)
    polygon = fields.ForeignKeyField("models.Polygons", related_name="metric_polygons")
    metric_name = fields.CharField(max_length=100)
    values = fields.JSONField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class MetricPolygonsItems(Model):
    item_id = fields.IntField(pk=True)
    metric_polygon = fields.ForeignKeyField(
        "models.MetricPolygons", related_name="items"
    )
    raster_data = fields.BinaryField(null=True)  # Ajusta el tipo si es diferente
    created_at = fields.DatetimeField(auto_now_add=True)


class PrecalculatedAreas(Model):
    id = fields.IntField(pk=True)
    polygon = fields.ForeignKeyField("models.Polygons", related_name="precalculated_areas")
    area_id = fields.CharField(max_length=100)
    area_type = fields.CharField(max_length=50)
    created_at = fields.DatetimeField(auto_now_add=True)
