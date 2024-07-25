from fastapi import APIRouter, HTTPException, status

from app.services.auth_service import authenticate_user, create_access_token
from app.schemas.token import Token
from datetime import timedelta
from app.config import get_settings

router = APIRouter()
settings = get_settings()


@router.post("/token", response_model=Token)
async def login_for_access_token():
    user = authenticate_user()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Internal authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
