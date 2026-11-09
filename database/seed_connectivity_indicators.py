import csv
import logging
from typing import Dict

from app.models.models import ProtConn, DPC, Polygon, Collection
from app.services.utils.stac import fetch_collection_metadata
from database.seed_collections_and_metrics import CollectionEnum

logger = logging.getLogger(__name__)

PA_COLLECTIONS = [
    e.col_name
    for e in CollectionEnum
    if e.col_name.startswith("AreasProtegidas")
    and e.col_name != "AreasProtegidas"
]


async def seed_connectivity_indicators():
    await ProtConn.all().delete()
    await DPC.all().delete()

    with open("data/protconn.csv", "r", encoding="utf-8", newline="") as file:
        protconn_reader = csv.DictReader(file)
        list_objs = []
        for row in protconn_reader:
            polygon = await Polygon.get_or_none(official_code=row["geof_id"])
            prot_conn_obj = ProtConn(
                polygon=polygon,
                prot=0 if not row["Prot"] else row["Prot"],
                unprot=0 if not row["Unprotected"] else row["Unprotected"],
                prot_conn=0 if not row["ProtConn"] else row["ProtConn"],
                prot_unconn=(
                    0 if not row["ProtUnconn"] else row["ProtUnconn"]
                ),
            )
            list_objs.append(prot_conn_obj)

        if list_objs:
            await ProtConn.bulk_create(list_objs)
            logger.info(
                f"✔ {len(list_objs)} registros insertados de protconn",
            )
        else:
            logger.info(
                "⚠ No se insertaron registros de protconn. Verifica el archivo protconn.csv",
            )

    pa_names_by_id: Dict[int, str] = {}
    for collection_name in PA_COLLECTIONS:
        pa_collection = await Collection.get_or_none(name=collection_name)
        if not pa_collection:
            logger.info(
                f"⚠ No se encuentra la colección {collection_name} en la base de datos",
            )
            continue
        try:
            _, values, classes, _, _ = await fetch_collection_metadata(
                pa_collection
            )
        except Exception as e:
            logger.info(
                f"⚠ No se pudo obtener la metadata de {collection_name}: {e}",
            )
            continue
        pa_names_by_id.update(zip(values, classes))

    if not pa_names_by_id:
        logger.info(
            "⚠ No se pueden insertar registros de DPC, no se encontró ninguna colección de áreas protegidas",
        )
    else:
        errors = 0
        counter = 0
        with open("data/dpc.csv", "r", encoding="utf-8", newline="") as file:
            dpc_reader = csv.DictReader(file)
            for row in dpc_reader:
                if row["id"] == "NA":
                    print("id NA, %s" % (row["geofence_type"]))
                    errors += 1
                    continue
                if float(row["dPC"]) < 0:
                    print("dpc < 0, ignorando registro, %s" % (row))
                    errors += 1
                    continue
                polygon = await Polygon.get_or_none(official_code=row["id"])
                if not polygon:
                    print("polígono no encontrado, %s" % (row["id"]))
                    errors += 1
                    continue
                pa_name = pa_names_by_id.get(int(row["ap_id"]))
                if pa_name is None:
                    print(
                        "AP id no encontrada en el STAC, %s" % (row["ap_id"])
                    )
                    errors += 1
                    continue
                dpc_obj = DPC(
                    polygon=polygon,
                    dpc=row["dPC"],
                    pa_id=row["ap_id"],
                    pa_name=pa_name,
                    category=row["dpc_cat"],
                )
                await dpc_obj.save()
                counter += 1

            if counter > 0:
                logger.info(
                    f"✔ {counter} registros insertados de dpc",
                )
            else:
                print("errores: %s" % errors)
                logger.info(
                    "⚠ No se insertaron registros de dpc. Verifica el archivo dpc.csv",
                )
