import psycopg
import requests


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

GET_VALUES_POLYGON = "http://127.0.0.1:8000/metrics/{metric_id}/values/{polygon_id}"
GET_LAYER_POLYGON = "http://127.0.0.1:8000/metrics/{metric_id}/layer?polygon_id={polygon_id}&item_id={item_id}&class_id={class_id}"

# =========================
# Consultas
# =========================

POLYGONS_QUERY = """
    SELECT id
    FROM polygon
    ORDER BY id;
"""

METRICS_QUERY = """
    SELECT name
    FROM metric
    ORDER BY name;
"""

def get_polygons(conn):
    with conn.cursor() as cur:
        cur.execute(POLYGONS_QUERY)
        for row in cur:
            yield row[0]

def get_metrics(conn):
    with conn.cursor() as cur:
        cur.execute(METRICS_QUERY)
        for row in cur:
            yield row[0]

def call_api_values(polygon_id, metric_id):
    url = GET_VALUES_POLYGON.format(
        polygon_id=polygon_id,
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

def call_api_layer(polygon_id, metric_id, item_id, class_id):
    url = GET_LAYER_POLYGON.format(
        polygon_id=polygon_id,
        metric_id=metric_id,
        item_id=item_id,
        class_id=class_id
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
        metric = list(get_metrics(conn))
        log_result(f"metric encontradas: {len(metric)}")
        for polygon_id in get_polygons(conn):
            log_result(f"\n=== ID: {polygon_id} ===")
            for metric_id in metric:
                #Si alguna metrica es de las siguientes o el id del poligono es menor a 2, se omite la consulta de polygon_metric
                if (metric_id in ["persistenceHF", "sciPersistenceHF", "sciPersistenceHF_protectedAreas"]) or polygon_id < 2:
                    continue
                else:
                    log_result(
                        f"Consultando "
                        f"id={polygon_id}, "
                        f"name={metric_id}"
                    )
                    try:#Poblado de polygon_metric
                        response = call_api_values(
                            polygon_id,
                            metric_id,
                        )
                        log_result(
                            f"  Status: {response.status_code}"
                        )
                        if response.ok:
                            #Si alguna metrica es de las siguientes se omite la consulta de polygon_metric_layer
                            if metric_id in ["dpc", "statsOnSpecies", "currentHF_average", "currenrRecordsGaps_average", "timelineHF", "protectedAreas", "protectedAreas_paramo", "protectedAreas_tropicalDryForest", "protectedAreas_wetland", "protConn"]:
                                continue
                            else:    
                                data = response.json()
                                if isinstance(data, dict):
                                    objects = [data]
                                elif isinstance(data, list):
                                    objects = data
                                else:
                                    objects = []
                                try:
                                    for obj in objects:
                                        item_id = obj.get("id")
                                        for key, value in obj.items():
                                            if key == "id":
                                                continue
                                            class_id = key
                                            if metric_id in ["recordGaps", "richness"]:
                                                class_id = metric_id
                                            log_result(
                                                f"    item_id : {item_id}, "
                                                f"class_id : {class_id}"
                                            )
                                            try:#Poblado de polygon_metric_layer
                                                response = call_api_layer(
                                                    polygon_id,
                                                    metric_id,
                                                    item_id,
                                                    class_id
                                                )
                                                log_result(
                                                    f"  Status: {response.status_code}"
                                                )
                                                if response.ok == False:
                                                    log_result(
                                                        f"  ERROR: {response.text}"
                                                    )
                                            except requests.RequestException as exc:
                                                log_result(
                                                    f"  ERROR de conexión: {exc}"
                                                )
                                except KeyError as ke:
                                    log_result(
                                        f"  ERROR: No hay item_id"
                                    )
                        else:
                            log_result(
                                f"  ERROR: {response.text}"
                            )
                    except requests.RequestException as exc:
                        log_result(
                            f"  ERROR de conexión: {exc}"
                        )


if __name__ == "__main__":
    main()
    print("Proceso finalizado.")