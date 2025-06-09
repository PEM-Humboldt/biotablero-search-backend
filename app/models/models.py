from tortoise import fields
from tortoise.models import Model


class AreaType(Model):
    id = fields.CharField(pk=True, max_length=50)
    label = fields.CharField(max_length=255)

    class Meta(Model.Meta):
        table = "area_type"


class Polygon(Model):
    id = fields.IntField(pk=True)
    hash = fields.CharField(max_length=255, unique=True, null=True)
    geometry = fields.JSONField()
    area_type = fields.ForeignKeyField(
        "bt_search_bk.AreaType",
        related_name="polygons",
        null=True,
        on_delete=fields.SET_NULL,
    )
    name = fields.CharField(max_length=255)
    area = fields.FloatField()
    official_code = fields.CharField(max_length=100, null=True)

    class Meta(Model.Meta):
        table = "polygon"
        indexes = [("hash",)]


class PolygonMetric(Model):
    id = fields.IntField(pk=True)
    metric = fields.CharField(max_length=100)
    values = fields.JSONField()
    polygon = fields.ForeignKeyField(
        "bt_search_bk.Polygon",
        related_name="metrics",
        on_delete=fields.CASCADE,
    )

    class Meta(Model.Meta):
        table = "polygon_metric"


class PolygonMetricItem(Model):
    id = fields.IntField(pk=True)
    metric = fields.CharField(max_length=100)
    polygon = fields.ForeignKeyField(
        "bt_search_bk.Polygon",
        related_name="metric_items",
        on_delete=fields.CASCADE,
    )
    layer_url = fields.CharField(max_length=255)
    category = fields.IntField()
    item_id = fields.CharField(max_length=100)

    class Meta(Model.Meta):
        table = "polygon_metric_item"
        unique_together = (("polygon", "metric", "category", "item_id"),)
