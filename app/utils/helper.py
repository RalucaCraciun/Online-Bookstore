import os

from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Set
from jose import jwt

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
SECRET_KEY = "ABC"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
TOKEN_BLACKLIST: Set[str] = set()


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def is_token_blacklisted(token: str) -> bool:
    """
    Check if the token is blacklisted.
    """
    return token in TOKEN_BLACKLIST
