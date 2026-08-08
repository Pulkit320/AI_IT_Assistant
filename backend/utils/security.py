"""
Security Utilities Module.
Handles password hashing via PassLib Bcrypt and JWT token encoding/decoding via python-jose.
"""

from datetime import datetime, timedelta
from typing import Optional, Any
from jose import jwt, JWTError
from passlib.context import CryptContext
from backend.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against a stored Bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generates a secure Bcrypt hash for a plain text password."""
    return pwd_context.hash(password)


def create_access_token(subject: str | Any, expires_delta: Optional[timedelta] = None) -> str:
    """Encodes subject and expiration into a signed JWT access token string."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[str]:
    """Decodes JWT access token and returns subject if signature is valid."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
