from tortoise import fields
from tortoise.models import Model


class Polygons(Model):
    id = fields.IntField(pk=True)
    polygon_geometry = fields.JSONField()
    polygon_hash = fields.CharField(max_length=64, unique=True, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta(Model.Meta):
        table = "polygons"
        indexes = [
            ("polygon_hash",),
        ]


class MetricPolygons(Model):
    id = fields.IntField(pk=True)
    polygon = fields.ForeignKeyField(
        "models.Polygons", related_name="metric_polygons"
    )
    metric_name = fields.CharField(max_length=100)
    values = fields.JSONField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta(Model.Meta):
        table = "metric_polygons"


class MetricPolygonsItems(Model):
    id = fields.IntField(pk=True)
    metric_polygon = fields.ForeignKeyField(
        "models.MetricPolygons", related_name="items"
    )
    raster_data = fields.BinaryField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta(Model.Meta):
        table = "metric_polygons_items"


class PrecalculatedAreas(Model):
    id = fields.IntField(pk=True)
    polygon = fields.ForeignKeyField(
        "models.Polygons", related_name="precalculated_areas"
    )
    area_id = fields.CharField(max_length=100)
    area_type = fields.CharField(max_length=50)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta(Model.Meta):
        table = "precalculated_areas"
