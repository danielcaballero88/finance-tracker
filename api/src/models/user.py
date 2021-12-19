from typing import Optional

import fastapi as fa
import pydantic as pyd

import auth

FAKE_USERS_DB = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashed_secret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "email": "alice@example.com",
        "hashed_password": "fakehashed_secret2",
        "disabled": True,
    },
}


class User(pyd.BaseModel):
    username: str
    email: str


class UserInDB(User):
    hashed_password: str
    disabled: bool


def fake_create_token(user: UserInDB) -> str:
    """Example AND FAKE token creating function.

    The token is created based on username and password.
    """
    token = user.username + "___" + user.hashed_password
    return token


def fake_decode_token(token: str) -> Optional[UserInDB]:
    """
    Example AND FAKE token decoding function.
    The idea of decoding a token is:
        token -> user
    """
    username = token.split("___")[0]
    user = get_user_by_username(FAKE_USERS_DB, username)
    return user


def fake_hash_password(password: str):
    """Example AND FAKE password hashing function."""
    return "fakehashed_" + password


def get_user_by_username(db, username: str) -> Optional[UserInDB]:
    """Gets a user from the DB by username."""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    else:
        return None


def get_current_user(
    token: str = fa.Depends(auth.shared.oauth2_scheme),
) -> Optional[UserInDB]:
    """Gets the current user according to the bearer token."""
    print("get_current_user")
    curr_usr_in_db = fake_decode_token(token)

    if curr_usr_in_db is None:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return curr_usr_in_db


def get_current_active_user(
    curr_usr_in_db: UserInDB = fa.Depends(get_current_user),
) -> User:
    """Gets the current user (if active) according to the token."""
    print("get_current_active_user")
    if curr_usr_in_db.disabled:
        raise fa.HTTPException(status_code=400, detail="Inactive user")

    curr_usr = User(**curr_usr_in_db.dict())
    return curr_usr
