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
    official_code = fields.CharField(max_length=100, unique=True, null=True)

    class Meta(Model.Meta):
        table = "polygon"
        indexes = [("hash",)]


class PolygonMetric(Model):
    id = fields.IntField(pk=True)
    values = fields.JSONField()
    polygon = fields.ForeignKeyField(
        "bt_search_bk.Polygon",
        related_name="metrics",
        on_delete=fields.CASCADE,
    )
    metric = fields.ForeignKeyField(
        "bt_search_bk.Metric",
        related_name="polygon_metrics",
        on_delete=fields.CASCADE,
    )

    class Meta(Model.Meta):
        table = "polygon_metric"


class PolygonMetricItem(Model):
    id = fields.IntField(pk=True)
    polygon = fields.ForeignKeyField(
        "bt_search_bk.Polygon",
        related_name="metric_items",
        on_delete=fields.CASCADE,
    )
    layer_url = fields.CharField(max_length=255)
    category = fields.IntField()
    item_id = fields.CharField(max_length=100)
    metric = fields.ForeignKeyField(
        "bt_search_bk.Metric",
        related_name="metric_items",
        on_delete=fields.CASCADE,
    )

    class Meta(Model.Meta):
        table = "polygon_metric_item"
        unique_together = (("polygon", "metric", "category", "item_id"),)


class Collection(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    updated_at = fields.DatetimeField()

    class Meta(Model.Meta):
        table = "collection"


class Metric(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    operation_type = fields.CharField(max_length=100, null=False)

    class Meta(Model.Meta):
        table = "metric"


class MetricCollection(Model):
    id = fields.IntField(pk=True)
    is_primary = fields.BooleanField()
    metric = fields.ForeignKeyField(
        "bt_search_bk.Metric",
        related_name="collections",
        on_delete=fields.CASCADE,
    )
    collection = fields.ForeignKeyField(
        "bt_search_bk.Collection",
        related_name="metrics",
        on_delete=fields.CASCADE,
    )

    class Meta(Model.Meta):
        table = "metric_collection"
