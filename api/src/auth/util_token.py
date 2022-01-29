from datetime import datetime, timedelta
from typing import Optional

import fastapi as fa
import jose
import pydantic as pyd
from jose import jwt

SECRET_KEY = "8331c1ea34b83cb53c33687503402982cf86a54e0efccfaf588fa9e3cb545eb2"
ALGORITHM = "HS256"
DEFAULT_EXPIRES_DELTA = timedelta(minutes=30)

credentials_exception = fa.HTTPException(
    status_code=fa.status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class Token(pyd.BaseModel):
    access_token: str
    token_type: str


class TokenData(pyd.BaseModel):
    username: Optional[str] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates an access new access token."""
    expire = datetime.utcnow() + (expires_delta or DEFAULT_EXPIRES_DELTA)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> TokenData:
    """Decodes a bearer token to get the username.

    The bearer token is decoded using `jwt.decode` and the username
    is extracted and returned in a TokenData object (pydantic model).

    Args:
        token (str): A bearer token.

    Returns:
        token_data (TokenData): A pydantic model with the username.

    Raises:
        fa.status.HTTPException: "401 Unauthorized" exception if any
            `jose.JWTError` occurs or if the username is not within the
            token under the key "sub".
    """
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jose.JWTError:
        raise credentials_exception
    else:
        return token_data
