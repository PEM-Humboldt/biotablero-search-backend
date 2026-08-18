from tortoise import fields
from tortoise.models import Model


class AreaType(Model):
    id = fields.CharField(pk=True, max_length=50)
    label = fields.CharField(max_length=255, unique=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta(Model.Meta):
        table = "area_type"


class Polygon(Model):
    id = fields.IntField(pk=True)
    hash = fields.CharField(max_length=255, unique=True, null=True)
    geometry = fields.JSONField()
    area_type = fields.ForeignKeyField(
        "bt_search_bk.AreaType",
        related_name="polygons",
        null=False,
        on_delete=fields.CASCADE,
    )
    name = fields.CharField(max_length=255, null=True)
    area = fields.FloatField()
    official_code = fields.CharField(max_length=100, unique=True, null=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta(Model.Meta):
        table = "polygon"
        indexes = [("hash",)]


class PolygonMetric(Model):
    id = fields.IntField(pk=True)
    values = fields.JSONField()
    group = fields.CharField(max_length=100, default="total")
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
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta(Model.Meta):
        table = "polygon_metric"
        unique_together = ("polygon", "metric", "group")


class PolygonMetricLayer(Model):
    id = fields.IntField(pk=True)
    metric = fields.ForeignKeyField(
        "bt_search_bk.Metric",
        related_name="metric_items",
        on_delete=fields.CASCADE,
    )
    polygon = fields.ForeignKeyField(
        "bt_search_bk.Polygon",
        related_name="metric_items",
        on_delete=fields.CASCADE,
    )
    class_id = fields.CharField(max_length=100)
    item_id = fields.CharField(max_length=100)
    layer_url = fields.CharField(max_length=255)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta(Model.Meta):
        table = "polygon_metric_item"
        unique_together = (
            (
                "metric",
                "polygon",
                "item_id",
                "class_id",
            ),
        )


class Collection(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    updated_at = fields.DatetimeField(auto_now=True)

    metrics: fields.ReverseRelation["MetricCollection"]

    class Meta(Model.Meta):
        table = "collection"


class Metric(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    operation_type = fields.CharField(max_length=100)
    allows_national = fields.BooleanField(default=False)
    updated_at = fields.DatetimeField(auto_now=True)
    indicator_card_id = fields.CharField(max_length=60, null=True)

    collections: fields.ReverseRelation["MetricCollection"]
    indicator: fields.ReverseRelation["MetricIndicator"]
    info: fields.ReverseRelation["MetricInfo"]

    class Meta(Model.Meta):
        table = "metric"


class MetricCollection(Model):
    id = fields.IntField(pk=True)
    is_primary = fields.BooleanField()
    group_name = fields.CharField(max_length=100, null=True)
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
    updated_at = fields.DatetimeField(auto_now=True)

    metric_id: fields.ForeignKeyRelation["Metric"]
    collection_id: fields.ForeignKeyRelation["Collection"]

    class Meta(Model.Meta):
        table = "metric_collection"


class MetricIndicator(Model):
    id = fields.IntField(pk=True)
    metric = fields.ForeignKeyField(
        "bt_search_bk.Metric",
        related_name="indicator",
        on_delete=fields.CASCADE,
    )
    indicator = fields.CharField(max_length=100, unique=True)
    has_group = fields.BooleanField(default=False)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta(Model.Meta):
        table = "metric_indicator"


class MetricInfo(Model):
    id = fields.IntField(pk=True)
    metric = fields.ForeignKeyField(
        "bt_search_bk.Metric",
        related_name="info",
        on_delete=fields.CASCADE,
    )
    type = fields.CharField(max_length=100)
    description = fields.TextField()
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta(Model.Meta):
        table = "metric_info"


class ProtConn(Model):
    id = fields.IntField(pk=True)
    polygon = fields.ForeignKeyField(
        "bt_search_bk.Polygon",
        related_name="prot_conn",
        on_delete=fields.CASCADE,
    )
    prot = fields.FloatField()
    unprot = fields.FloatField()
    prot_conn = fields.FloatField()
    prot_unconn = fields.FloatField()
    updated_at = fields.DatetimeField(auto_now=True)

    def get_result_for_metric(self):
        return {
            "id": "protConn",
            "prot": self.prot,
            "unprot": self.unprot,
            "prot_conn": self.prot_conn,
            "prot_unconn": self.prot_unconn,
        }

    class Meta(Model.Meta):
        table = "prot_conn"


class DPC(Model):
    id = fields.IntField(pk=True)
    polygon = fields.ForeignKeyField(
        "bt_search_bk.Polygon",
        related_name="dpc",
        on_delete=fields.CASCADE,
    )
    dpc = fields.FloatField()
    pa_id = fields.IntField()
    pa_name = fields.CharField(max_length=150)
    category = fields.CharField(max_length=150)
    updated_at = fields.DatetimeField(auto_now=True)

    def get_result_for_metric(self):
        return {
            "id": str(self.id),
            "dpc": self.dpc,
            "pa_id": self.pa_id,
            "pa_name": self.pa_name,
            "category": self.category,
        }

    class Meta(Model.Meta):
        table = "dpc"


class SpeciesStats(Model):
    id = fields.IntField(pk=True)
    polygon = fields.ForeignKeyField(
        "bt_search_bk.Polygon",
        related_name="species_stats",
        on_delete=fields.CASCADE,
    )
    group_name = fields.CharField(max_length=100)
    total = fields.IntField()
    threatened_total = fields.IntField()
    threatened_cr = fields.IntField()
    threatened_en = fields.IntField()
    threatened_vu = fields.IntField()
    invasive = fields.IntField()
    endemic = fields.IntField()
    endemic_threatened = fields.IntField()
    updated_at = fields.DatetimeField(auto_now=True)

    def get_result_for_metric(self):
        return {
            "total": self.total,
            "threatened_total": self.threatened_total,
            "threatened_cr": self.threatened_cr,
            "threatened_en": self.threatened_en,
            "threatened_vu": self.threatened_vu,
            "invasive": self.invasive,
            "endemic": self.endemic,
            "endemic_threatened": self.endemic_threatened,
        }

    class Meta(Model.Meta):
        table = "species_stats"
