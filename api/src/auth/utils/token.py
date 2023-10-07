"""Token utility module."""

import datetime as dt
from typing import Optional, TypedDict, cast

import fastapi as fa
import jose
import pydantic as pyd
from jose import jwt

SECRET_KEY = "8331c1ea34b83cb53c33687503402982cf86a54e0efccfaf588fa9e3cb545eb2"
ALGORITHM = "HS256"
DEFAULT_EXPIRES_DELTA = dt.timedelta(minutes=30)

credentials_exception = fa.HTTPException(
    status_code=fa.status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class Token(pyd.BaseModel):
    token_type: str
    token: str
    expiration: dt.datetime


class TokenData(pyd.BaseModel):
    """Model for the data stored in a token."""

    username: str
    expiration: dt.datetime


class TokenCreateDict(TypedDict):
    """Typed dict for the data needed to create a token."""

    sub: str
    exp: dt.datetime


def create_access_token(
    username: str, expires_delta: Optional[dt.timedelta] = None
) -> Token:
    """Creates a new access token."""
    expire = dt.datetime.utcnow() + (expires_delta or DEFAULT_EXPIRES_DELTA)

    to_encode = TokenCreateDict(sub=username, exp=expire)

    encoded_jwt: str = jwt.encode(
        cast(dict, to_encode),
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    token = Token(token_type="bearer", token=encoded_jwt, expiration=expire)

    return token


def decode_token(token: str) -> TokenData:
    """Decodes a bearer token to get the username.

    The bearer token is decoded using `jwt.decode` and the username
    is extracted and returned in a TokenData object.

    Args:
        token (str): A bearer token.

    Returns:
        token_data (TokenData): An object with the username and
            expiration datetime in UTC.

    Raises:
        fa.status.HTTPException: "401 Unauthorized" exception if any
            `jose.JWTError` occurs or if the username is not within the
            token under the key "sub".
    """
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        sub = payload.get("sub")
        exp = payload.get("exp")
        if sub is None or exp is None:
            raise credentials_exception

        username: str = sub
        expiration = dt.datetime.fromtimestamp(exp)

        token_data = TokenData(username=username, expiration=expiration)
    except jose.JWTError:
        raise credentials_exception
    else:
        return token_data
