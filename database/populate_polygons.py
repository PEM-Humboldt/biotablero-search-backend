import psycopg
import requests

API_BASE_URL = "http://127.0.0.1:8000"
# =========================
# PostgreSQL
# =========================

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "search",
    "user": "bt-back",
    "password": "bt-back",
}

# =========================
# API
# =========================

GET_METRIC_GROUPS = "{api_base}/metrics/{metric_id}/groups"
GET_VALUES_POLYGON = (
    "{api_base}/metrics/{metric_id}/values/{polygon_id}?group={group}"
)
GET_LAYER_POLYGON = "{api_base}/metrics/{metric_id}/layer?polygon_id={polygon_id}&item_id={item_id}&class_id={class_id}&group={group}"

# =========================
# Consultas
# =========================
QUERY = "SELECT {select_columns} FROM {from_table} ORDER BY {order_column}"


def get_query(conn, select_columns, from_table, order_column):
    with conn.cursor() as cur:
        cur.execute(
            QUERY.format(
                select_columns=select_columns,
                from_table=from_table,
                order_column=order_column,
            )
        )
        for row in cur:
            yield row[0]


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
    print(text)
    with open("./logs/populate_polygons_res.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")


def main():
    print("Proceso Iniciado.")
    with psycopg.connect(**DB_CONFIG) as conn:
        metrics = list(get_query(conn, "name", "metric", "name"))
        polygons = list(get_query(conn, "id", "polygon", "id"))
        log_result(f"metric encontradas: {len(metrics)}")
        log_result(f"polygons encontrados: {len(polygons)}")
        for metric_id in metrics:
            # Si alguna metrica es de las siguientes se omite la consulta de polygon_metric
            if metric_id in [
                "persistenceHF",
                "sciPersistenceHF",
                "sciPersistenceHF_protectedAreas",
            ]:
                continue
            else:
                log_result(f"\n=== Metric: {metric_id} ===")
                try:
                    # Consulta de grupos de metricas
                    log_result(
                        f"Consultando grupos de la metrica {metric_id} "
                    )
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
                    else:
                        log_result(f"  Metrica sin grupo.")
                    for group in groups:
                        log_result(f"  group : {group}")
                        for polygon_id in get_query(
                            conn, "id", "polygon", "id"
                        ):
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


if __name__ == "__main__":
    main()
    print("Proceso finalizado.")
