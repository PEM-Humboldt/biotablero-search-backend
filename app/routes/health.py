from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    """Simple liveness probe. Returns 200 if the process is up."""
    return {"status": "ok"}
