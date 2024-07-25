from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt, ExpiredSignatureError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.config import get_settings
from app.schemas.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
settings = get_settings()


def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password


def get_user(username: str):
    fake_users_db = {
        settings.user_username: {"username": settings.user_username, "hashed_password": settings.user_hashed_password}
    }
    return fake_users_db.get(username)


def authenticate_user():
    return {"username": settings.user_username}


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt
