from app.models.models import AreaType


async def seed_area_types():
    if await AreaType.all().count() == 0:
        area_types = [
            AreaType(id="states", label="Departamentos"),
            AreaType(id="ea", label="Jurisdicciones Ambientales"),
            AreaType(id="basinSubzones", label="Subzonas Hidrográficas"),
            AreaType(id="paramos", label="Páramos"),
            AreaType(id="input", label="Polígono"),
        ]
        await AreaType.bulk_create(area_types)
