from tortoise import Tortoise
from database.seed_area_types import seed_area_types
from app.utils.config import TORTOISE_ORM


async def populate_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)
    await seed_area_types()
