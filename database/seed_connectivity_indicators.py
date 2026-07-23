import csv
import logging

from app.models.models import ProtConn, DPC, Polygon, Collection
from app.services.utils.stac import fetch_collection_metadata

logger = logging.getLogger(__name__)


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

    pa_collection = await Collection.get_or_none(name="AreasProtegidas")
    if not pa_collection:
        logger.info(
            "⚠ No se pueden insertar registros de DPC, no se encuentra la colección de áreas protegidas en la base de datos",
        )
    else:
        errors = 0
        counter = 0
        _, values, classes, _, _ = await fetch_collection_metadata(
            pa_collection
        )
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
                pa_index = None
                try:
                    pa_index = values.index(int(row["ap_id"]))
                except ValueError as e:
                    print(
                        "AP id no encontrada en el STAC, %s" % (row["ap_id"])
                    )
                    continue
                pa_name = classes[pa_index]
                dpc_obj = DPC(
                    polygon=polygon,
                    dpc=row["dPC"],
                    pa_id=row["ap_id"],
                    pa_name=pa_name,
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
