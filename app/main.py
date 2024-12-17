import subprocess
from contextlib import asynccontextmanager
from logging import getLogger
from typing import AsyncGenerator

from fastapi import FastAPI, exceptions
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from app.middleware.exception_handlers import (
    validation_exception_handler,
    server_exception_handler,
    not_found_exception_handler,
)
from app.routes import migrations
from app.utils.errors import ServerError, NotFoundError
from app.middleware.log_middleware import log_requests
from app.routes import metrics
from app.utils import context_vars
from app.utils.config import get_settings, init_tortoise
from app.services.migrations import (
    run_aerich_migrate,
    run_aerich_upgrade,
    run_aerich_init,
)

settings = get_settings()
settings.configure_logging()
logger = getLogger(__name__)
request_id_context = context_vars.request_id_context


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await init_tortoise()

    try:
        logger.info(
            "Inicializando Aerich...",
            extra={"request_id": request_id_context.get()},
        )
        init_result = run_aerich_init()
        logger.info(
            init_result, extra={"request_id": request_id_context.get()}
        )

        migration_result = run_aerich_migrate()
        logger.info(
            f"Resultado de migraciones: {migration_result}",
            extra={"request_id": request_id_context.get()},
        )

        upgrade_result = run_aerich_upgrade()
        logger.info(
            f"Resultado de actualización: {upgrade_result}",
            extra={"request_id": request_id_context.get()},
        )

    except subprocess.CalledProcessError as e:
        logger.error(
            f"Error al ejecutar un comando de Aerich: {e}",
            extra={"request_id": request_id_context.get()},
        )
        if e.output:
            logger.error(
                f"Salida del error: {e.output.decode()}",
                extra={"request_id": request_id_context.get()},
            )
        raise Exception("Error al ejecutar un comando de Aerich.")
    except Exception as e:
        logger.error(
            f"Error inesperado: {e}",
            extra={"request_id": request_id_context.get()},
        )
        raise

    yield

    logger.info(
        "Cerrando conexiones de Tortoise...",
        extra={"request_id": request_id_context.get()},
    )
    await Tortoise.close_connections()


app = FastAPI(
    title="BioTableroSearch",
    description="Get metrics by predefined or custom (polygon) areas.",
    summary="Metrics for BioTablero Search module",
    version="0.1.0",
    contact={
        "name": "Equipo BioTablero",
        "url": "http://biotablero.humboldt.org.co/",
        "email": "biotablero@humboldt.org.co",
    },
    docs_url=None if settings.env.lower() == "prod" else "/docs",
    lifespan=lifespan,
)

app.middleware("http")(log_requests)

app.add_exception_handler(
    exceptions.RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    exceptions.ValidationException,
    validation_exception_handler,
)

app.add_exception_handler(NotFoundError, not_found_exception_handler)
app.add_exception_handler(ServerError, server_exception_handler)
app.add_exception_handler(Exception, server_exception_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(metrics.router)
app.include_router(migrations.router)
