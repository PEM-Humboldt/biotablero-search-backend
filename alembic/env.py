from dotenv import load_dotenv
import os
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context
from app.utils.config import get_settings
from app.db.base import Base


config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata

load_dotenv()

settings = get_settings()

try:
    SYNC_DATABASE_URL = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}/{settings.postgres_db}"

except AttributeError:
    raise ValueError("DATABASE_URL_SYNC is not set in the environment")


def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and name == "spatial_ref_sys":
        return False
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=SYNC_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = config.attributes.get("connection", None)
    if connectable is None:
        # If no connection is provided, generate one from the
        # connection string
        connectable = create_engine(SYNC_DATABASE_URL)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
