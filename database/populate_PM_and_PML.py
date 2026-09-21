import requests
import logging
import asyncio
from tortoise import Tortoise
from app.models.models import (
    Metric,
    Polygon,
    PolygonMetric,
    PolygonMetricLayer,
)
from app.utils.config import get_settings, TORTOISE_ORM

settings = get_settings()
logger = logging.getLogger(__name__)

# =========================
# Consultas POSTGRESQL
# =========================
DB_CONFIG = {
    "host": settings.db_host,
    "port": settings.db_port,
    "dbname": settings.db_name,
    "user": settings.db_user,
    "password": settings.db_password,
}


async def get_metrics():
    return (
        await Metric.all()
        .order_by("id")
        .values_list(
            "name",
            flat=True,
        )
    )


async def get_polygons():
    return (
        await Polygon.all()
        .order_by("id")
        .values_list(
            "id",
            flat=True,
        )
    )


async def get_polygon_metric():
    return (
        await PolygonMetric.all()
        .order_by("id")
        .values_list(
            "id",
            flat=True,
        )
    )


async def get_polygon_metric_layer():
    return (
        await PolygonMetricLayer.all()
        .order_by("id")
        .values_list(
            "id",
            flat=True,
        )
    )


# =========================
# CONSULTAS API
# =========================
API_BASE_URL = settings.api_base_url
GET_METRIC_GROUPS = "{api_base}/metrics/{metric_id}/groups"
GET_VALUES_POLYGON = (
    "{api_base}/metrics/{metric_id}/values/{polygon_id}?group={group}"
)
GET_LAYER_POLYGON = "{api_base}/metrics/{metric_id}/layer?polygon_id={polygon_id}&item_id={item_id}&class_id={class_id}&group={group}"


def call_api_groups(api_base, metric_id):
    url = GET_METRIC_GROUPS.format(
        api_base=api_base,
        metric_id=metric_id,
    )
    log_result(f"  URL: {url}")
    response = requests.get(
        url,
        headers={
            "accept": "application/json",
        },
    )
    return response


def call_api_values(api_base, polygon_id, metric_id, group):
    url = GET_VALUES_POLYGON.format(
        api_base=api_base,
        polygon_id=polygon_id,
        metric_id=metric_id,
        group=group,
    )
    log_result(f"  URL: {url}")
    response = requests.get(
        url,
        headers={
            "accept": "application/json",
        },
    )
    return response


def call_api_layer(api_base, polygon_id, metric_id, item_id, class_id, group):
    url = GET_LAYER_POLYGON.format(
        api_base=api_base,
        polygon_id=polygon_id,
        metric_id=metric_id,
        item_id=item_id,
        class_id=class_id,
        group=group,
    )
    log_result(f"  URL: {url}")
    response = requests.get(
        url,
        headers={
            "accept": "application/json",
        },
    )
    return response


def log_result(text):
    with open("./logs/populate_polygons_res.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")


async def populate_PM_and_PML():
    await Tortoise.init(config=TORTOISE_ORM)
    try:
        metrics = await get_metrics()
        polygons = await get_polygons()
        print(f"metric encontradas: {len(metrics)}")
        print(f"polygons encontrados: {len(polygons)}")
        for metric_id in metrics:
            # Si alguna metrica es de las siguientes se omite la consulta de polygon_metric
            if metric_id in [
                "persistenceHF",
                "sciPersistenceHF",
                "sciPersistenceHF_protectedAreas",
            ]:
                continue
            else:
                print(f"\n=== Metric: {metric_id} ===")
                log_result(f"\n=== Metric: {metric_id} ===")
                try:
                    # Consulta de grupos de metricas
                    print(f"  Consultando grupos de la metrica {metric_id} ")
                    response = call_api_groups(
                        api_base=API_BASE_URL, metric_id=metric_id
                    )
                    log_result(f"  Status: {response.status_code}")
                    groups = [""]
                    if response.ok:
                        data = response.json()
                        if isinstance(data, list):
                            groups = groups + data
                        else:
                            log_result(
                                f"  ERROR: Respuesta inesperada: {data}"
                            )
                    print(f"  groups: {groups}")
                    for group in groups:
                        print(f"  Consultando group : {group}")
                        log_result(f"  Consultando group : {group}")
                        for polygon_id in polygons:
                            try:
                                # Poblado de polygon_metric
                                response = call_api_values(
                                    api_base=API_BASE_URL,
                                    polygon_id=polygon_id,
                                    metric_id=metric_id,
                                    group=group,
                                )
                                log_result(f"  Status: {response.status_code}")
                                if response.ok:
                                    # Si alguna metrica es de las siguientes se omite la consulta de polygon_metric_layer
                                    if metric_id in [
                                        "dpc",
                                        "statsOnSpecies",
                                        "currentHF_average",
                                        "recordGaps_averages",
                                        "timelineHF",
                                        "protectedAreas",
                                        "protectedAreas_paramo",
                                        "protectedAreas_tropicalDryForest",
                                        "protectedAreas_wetland",
                                        "protConn",
                                    ]:
                                        continue
                                    else:
                                        data = response.json()
                                        if isinstance(data, dict):
                                            objects = [data]
                                        elif isinstance(data, list):
                                            objects = data
                                        else:
                                            log_result(
                                                f"  ERROR: Respuesta inesperada: {data}"
                                            )
                                            continue
                                        for obj in objects:
                                            item_id = obj.get("id")
                                            for key, value in obj.items():
                                                if key == "id":
                                                    continue
                                                class_id = key
                                                if metric_id in [
                                                    "recordGaps",
                                                    "richness",
                                                ]:
                                                    class_id = metric_id
                                                log_result(
                                                    f"    item_id : {item_id}, "
                                                    f"class_id : {class_id}"
                                                )
                                                try:  # Poblado de polygon_metric_layer
                                                    response = call_api_layer(
                                                        api_base=API_BASE_URL,
                                                        polygon_id=polygon_id,
                                                        metric_id=metric_id,
                                                        item_id=item_id,
                                                        class_id=class_id,
                                                        group=group,
                                                    )
                                                    log_result(
                                                        f"  Status: {response.status_code}"
                                                    )
                                                    if response.ok == False:
                                                        log_result(
                                                            f"  ERROR: {response.text}"
                                                        )
                                                except (
                                                    requests.RequestException
                                                ) as exc:
                                                    log_result(
                                                        f"  ERROR de conexión: {exc}"
                                                    )
                                else:
                                    log_result(f"  ERROR: {response.text}")
                            except requests.RequestException as exc:
                                log_result(f"  ERROR de conexión: {exc}")
                except requests.RequestException as exc:
                    log_result(f"  ERROR de conexión: {exc}")
    except Exception as e:
        log_result(f"  ERROR: {e}")

    polygon_metric_count = await get_polygon_metric()
    polygon_metric_layer_count = await get_polygon_metric_layer()
    print(f"\npolygon_metric encontrados: {len(polygon_metric_count)}")
    print(
        f"polygon_metric_layer encontrados: {len(polygon_metric_layer_count)}"
    )
    await Tortoise.close_connections()
    logger.info(
        "Proceso finalizado, la conexión a la base de datos ha sido cerrada",
        extra={"request_id": "N/A"},
    )


if __name__ == "__main__":
    print(
        "Proceso de población de polygon_metric y polygon_metric_layer iniciado..."
    )
    asyncio.run(populate_PM_and_PML())
    print("Proceso de población finalizado.")
