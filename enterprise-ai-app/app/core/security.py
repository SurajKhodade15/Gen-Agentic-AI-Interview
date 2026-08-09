from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from app.core.config import get_settings

bearer = HTTPBearer()


def create_access_token(subject: str, roles: list[str]) -> str:
    cfg = get_settings()
    payload = {"sub": subject, "roles": roles, "exp": datetime.now(timezone.utc) + timedelta(minutes=cfg.access_token_expire_minutes)}
    return jwt.encode(payload, cfg.jwt_secret, algorithm=cfg.jwt_algorithm)


def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    cfg = get_settings()
    try:
        claims = jwt.decode(credentials.credentials, cfg.jwt_secret, algorithms=[cfg.jwt_algorithm])
        if not claims.get("sub"):
            raise JWTError()
        return claims
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from exc
