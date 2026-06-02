from datetime import datetime, timedelta, timezone
from passlib.hash import pbkdf2_sha256
from jose import JWTError, jwt
from app.core.config import get_settings

settings = get_settings()

def password_hasher(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pbkdf2_sha256.verify(
        password,
        hashed_password
    )


def create_token(data: dict, expire_delta: timedelta | None = None) -> str:
    if not settings.secret_key:
        raise ValueError("SECRET_KEY is required to create access tokens")

    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + (
        expire_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> dict | None:
    if not settings.secret_key:
        return None

    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        return None
