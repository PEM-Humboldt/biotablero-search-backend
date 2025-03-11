from app.models.models import AreaType


async def seed_area_types():
    if not await AreaType.all().count():
        await AreaType.get_or_create(
            id="states", defaults={"label": "Departamentos"}
        )
        await AreaType.get_or_create(
            id="ea", defaults={"label": "Jurisdicciones Ambientales"}
        )
        await AreaType.get_or_create(
            id="basinSubzones", defaults={"label": "Subzonas Hidrográficas"}
        )
        await AreaType.get_or_create(
            id="paramos", defaults={"label": "Páramos"}
        )
        await AreaType.get_or_create(
            id="input", defaults={"label": "Polígono"}
        )
