from functools import lru_cache
from logging import getLogger

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.utils import context_vars
from app.utils.config import get_settings

logger = getLogger(__name__)
request_id_context = context_vars.request_id_context

USER_NAME_CLAIM = "username"
TOKEN_LEEWAY_SECONDS = 30

bearer_scheme = HTTPBearer(auto_error=False)


@lru_cache
def get_jwks_client() -> jwt.PyJWKClient:
    """
    JWKS client for the Keycloak realm, signing keys are cached between
    requests and refreshed when a token uses an unknown key.
    """
    settings = get_settings()
    return jwt.PyJWKClient(
        f"{settings.kc_issuer}/protocol/openid-connect/certs",
        cache_keys=True,
        timeout=settings.connect_timeout,
    )


def _unauthorized(log_msg: str) -> HTTPException:
    logger.warning(
        f"Authentication failed: {log_msg}",
        extra={"request_id": request_id_context.get()},
    )
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user_name(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    """
    Validates the Keycloak access token from the Authorization header and
    returns the user name in it.
    """
    if credentials is None:
        raise _unauthorized("missing bearer token")

    settings = get_settings()
    token = credentials.credentials

    try:
        signing_key = get_jwks_client().get_signing_key_from_jwt(token)
    except jwt.PyJWKClientConnectionError as e:
        logger.error(
            f"Could not fetch signing keys from IAM server: {e}",
            extra={"request_id": request_id_context.get()},
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable",
        )
    except jwt.PyJWTError as e:
        raise _unauthorized(f"signing key not found ({e})")

    try:
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=settings.kc_client,
            issuer=settings.kc_issuer,
            leeway=TOKEN_LEEWAY_SECONDS,
            options={"require": ["exp", "iat", "iss", "aud"]},
        )
    except jwt.PyJWTError as e:
        raise _unauthorized(f"invalid token ({e})")

    # ID and refresh tokens share issuer and audience, only access tokens
    # are accepted
    if claims.get("typ") != "Bearer":
        raise _unauthorized(f"unexpected token type ({claims.get('typ')})")

    user_name = claims.get(USER_NAME_CLAIM)
    if not isinstance(user_name, str) or not user_name:
        raise _unauthorized(f"missing '{USER_NAME_CLAIM}' claim")

    return user_name
