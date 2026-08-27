import psycopg
import requests
import time


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

IDS_QUERY = """
    SELECT id
    FROM polygon
    ORDER BY id;
"""

NAMES_QUERY = """
    SELECT name
    FROM metric
    ORDER BY name;
"""


def get_ids(conn):
    with conn.cursor() as cur:
        cur.execute(IDS_QUERY)

        for row in cur:
            yield row[0]


def get_names(conn):
    with conn.cursor() as cur:
        cur.execute(NAMES_QUERY)

        for row in cur:
            yield row[0]


def call_api_values(polygon_id, metric_id):
    url = GET_VALUES_POLYGON.format(
        polygon_id=polygon_id,
        metric_id=metric_id,
    )

    response = requests.get(
        url,
        headers={
            "accept": "application/json",
        },
        timeout=30,
    )

    return response

def call_api_layer(polygon_id, metric_id, item_id, class_id):
    url = GET_LAYER_POLYGON.format(
        polygon_id=polygon_id,
        metric_id=metric_id,
        item_id=item_id,
        class_id=class_id
    )

    response = requests.get(
        url,
        headers={
            "accept": "application/json",
        },
        timeout=30,
    )

    return response


def main():

    with psycopg.connect(**DB_CONFIG) as conn:

        # Guardamos los names porque los vamos a reutilizar
        names = list(get_names(conn))

        print(f"Names encontrados: {len(names)}")

        for polygon_id in get_ids(conn):

            print(f"\n=== ID: {polygon_id} ===")

            for metric_id in names:

                print(
                    f"Consultando "
                    f"id={polygon_id}, "
                    f"name={metric_id}"
                )

                try:

                    response = call_api_values(
                        polygon_id,
                        metric_id,
                    )

                    print(
                        f"  Status: {response.status_code}"
                    )

                    if response.ok:
                        print(
                            f"  OK: {response.text}"
                        )
                        data = response.json()
                         
                        try: 
                            item_id = data["id"]
                            
                            response_keys = [ key for key in data if key != "id" ]
                            
                            for key in response_keys:
                                class_id = key
                                print(
                                    f"    item_id : {item_id}, "
                                    f"class_id : {class_id}"
                                )
                                try:
                                    response = call_api_layer(
                                        polygon_id,
                                        metric_id,
                                        item_id,
                                        class_id
                                    )

                                    print(
                                        f"  Status: {response.status_code}"
                                    )

                                    if response.ok:
                                        print(
                                            f"  OK: {response.text}"
                                        )
                                    else:
                                        print(
                                            f"  ERROR: {response.text}"
                                        )

                                except requests.RequestException as exc:

                                    print(
                                        f"  ERROR de conexión: {exc}"
                                    )
                                time.sleep(1.0)                            
                        except KeyError as ke:
                            print(
                                f"  ERROR: No hay item_id"
                            )
                    else:
                        print(
                            f"  ERROR: {response.text}"
                        )

                except requests.RequestException as exc:

                    print(
                        f"  ERROR de conexión: {exc}"
                    )

                # Esperar un poco antes de la siguiente petición
                time.sleep(1)


if __name__ == "__main__":
    main()