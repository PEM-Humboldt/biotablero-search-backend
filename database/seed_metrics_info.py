import csv
import logging

from app.models.models import MetricInfo, Metric

logger = logging.getLogger(__name__)


async def seed_metrics_info():
    await MetricInfo.all().delete()

    with open(
        "data/metric_info.csv", "r", encoding="utf-8", newline=""
    ) as file:
        reader = csv.DictReader(file)
        list_objs = []
        errors = 0

        for row in reader:
            metric = await Metric.get_or_none(name=row["metric_name"])

            if not metric:
                logger.warning(
                    f"⚠ Métrica '{row['metric_name']}' no encontrada. Saltando registro."
                )
                errors += 1
                continue

            metric_info_obj = MetricInfo(
                metric=metric,
                type=row["type"],
                description=row["description"],
            )
            list_objs.append(metric_info_obj)

        if list_objs:
            await MetricInfo.bulk_create(list_objs)
            logger.info(
                f"✔ {len(list_objs)} registros insertados de metric_info",
            )
        else:
            logger.info(
                "⚠ No se insertaron registros de metric_info. Verifica el archivo metric_info.csv",
            )

        if errors > 0:
            logger.warning(
                f"⚠ Se encontraron {errors} errores durante la inserción"
            )
