from fastapi import FastAPI

from .routers import metrics


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
)


app.include_router(metrics.router)
# TODO: disable swagger on production: https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls
