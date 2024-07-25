from fastapi import Request, HTTPException, status
from jose import jwt, ExpiredSignatureError, JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.config import get_settings
from app.services.auth_service import get_user

settings = get_settings()


class MethodBasedAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/token":
            return await call_next(request)

        if request.method in ["POST", "PUT", "DELETE"]:
            token = request.headers.get("Authorization")
            if not token:
                print("Missing Authorization header")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Missing Authorization header"},
                    headers={"WWW-Authenticate": "Bearer"},
                )

            credentials_exception = HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

            try:
                token = token.split("Bearer ")[1]
                print(f"Token received: {token}")
                payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
                print(f"Payload decoded: {payload}")
                username: str = payload.get("sub")
                if username is None:
                    print("Username not found in token payload")
                    raise credentials_exception
                user = get_user(username)
                print(user)
                if user is None:
                    print("User not found")
                    raise credentials_exception
            except IndexError:
                print("Invalid token format")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid token format"},
                    headers={"WWW-Authenticate": "Bearer"},
                )
            except ExpiredSignatureError:
                print("Token has expired")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Token has expired"},
                    headers={"WWW-Authenticate": "Bearer"},
                )
            except JWTError as e:
                print(f"JWT error: {e}")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Could not validate credentials"},
                    headers={"WWW-Authenticate": "Bearer"},
                )
            except Exception as e:
                print(f"Unexpected error: {e}")
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"detail": str(e)},
                )

        response = await call_next(request)
        return response
