from app.models.models import AreaType


async def seed_area_types():
    await AreaType.all().delete()
    area_types = [
        AreaType(id="states", label="Departamentos"),
        AreaType(id="ea", label="Jurisdicciones Ambientales"),
        AreaType(id="basinSubzones", label="Subzonas Hidrográficas"),
        AreaType(id="se", label="Ecosistemas Estratégicos"),
        AreaType(id="custom", label="Consulta Personalizada"),
        AreaType(id="paramos", label="Páramos"),
    ]
    await AreaType.bulk_create(area_types)
