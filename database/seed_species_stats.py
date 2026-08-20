import csv
import logging
from pathlib import Path

from app.models.models import Polygon, SpeciesStats

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _as_int(value: str | None) -> int:
    return 0 if value in (None, "") else int(float(value))


def _normalize_code(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


async def seed_species_stats():
    await SpeciesStats.all().delete()

    created = 0
    skipped = 0
    with open(
        PROJECT_ROOT / "data" / "statsOnSpecies.csv",
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            polygon = None
            try:
                cod_region = _normalize_code(row.get("cod_region"))
                if cod_region:
                    polygon = await Polygon.get_or_none(
                        official_code=cod_region
                    )
                    if polygon is None:
                        polygon = await Polygon.get_or_none(
                            official_code__iexact=cod_region
                        )

                if polygon is None:
                    skipped += 1
                    continue

                await SpeciesStats.create(
                    polygon=polygon,
                    group=row["slug_grupo"].strip(),
                    total=_as_int(row["especies_region_total"]),
                    threatened_total=_as_int(
                        row["especies_amenazadas_mads_total"]
                    ),
                    threatened_cr=_as_int(row["especies_amenazadas_mads_cr"]),
                    threatened_en=_as_int(row["especies_amenazadas_mads_en"]),
                    threatened_vu=_as_int(row["especies_amenazadas_mads_vu"]),
                    invasive=_as_int(row["especies_invasoras"]),
                    endemic=_as_int(row["especies_endemicas"]),
                    endemic_threatened=_as_int(
                        row["especies_endemicas_amenazadas"]
                    ),
                )
                created += 1
            except Exception as exc:
                skipped += 1

    logger.info(f"✔ {created} registros insertados de species_stats")
    if skipped:
        logger.info(
            f"⚠ {skipped} filas de species_stats no se pudieron importar"
        )
