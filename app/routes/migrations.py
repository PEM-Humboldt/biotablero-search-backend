import subprocess

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services.migrations import run_aerich_migrate, run_aerich_upgrade

router = APIRouter(
    prefix="/migrate",
    tags=["migrate"],
    responses={
        404: {"description": "Not found"},
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "message": "An internal server error occurred.",
                    }
                },
            },
        },
    },
)

@router.get("/migrate")
async def migrate():
    """
    Run Aerich migrations and upgrades the database.
    """
    try:
        migration_result = run_aerich_migrate()
        upgrade_result = run_aerich_upgrade()

        return JSONResponse(
            content={
                "message": "Database migration and upgrade completed successfully.",
                "migrate": migration_result,
                "upgrade": upgrade_result,
            },
            status_code=200,
        )
    except subprocess.SubprocessError as e:
        return JSONResponse(
            content={
                "message": "Error occurred during database migration or upgrade.",
                "details": str(e),
            },
            status_code=500,
        )