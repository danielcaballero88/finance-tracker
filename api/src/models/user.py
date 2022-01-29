from typing import Optional

import fastapi as fa
import pydantic as pyd

import auth
import auth.util_password as ut_pass
import auth.util_token as ut_token

FAKE_USERS_DB = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$ntIsymX7KQFN8apAd584CuoTFVHtIK./0WEsWLrpiWZmHDHtA97RW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "email": "alice@example.com",
        "hashed_password": "fakehashed_secret2",
        "disabled": True,
    },
}


class UserSafe(pyd.BaseModel):
    username: str
    email: str


class UserCreate(UserSafe):
    password: str


class User(UserSafe):
    hashed_password: str
    disabled: bool


def fake_create_token(user: User) -> str:
    """Example AND FAKE token creating function.

    The token is created based on username and password.
    """
    token = user.username + "___" + user.hashed_password
    return token


def fake_decode_token(token: str) -> Optional[User]:
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


def get_user_by_username(db, username: str) -> Optional[User]:
    """Gets a user from the DB by username."""
    if username in db:
        user_dict = db[username]
        return User(**user_dict)
    else:
        return None


def get_current_user(
    token: str = fa.Depends(auth.oauth2_scheme),
) -> Optional[User]:
    """Gets the current user according to the bearer token."""
    # Decode token.
    token_data = ut_token.decode_token(token)
    # Get user.
    user = get_user_by_username(db=FAKE_USERS_DB, username=token_data.username)
    if user is None:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Done.
    return user


def get_current_active_user(
    curr_usr: User = fa.Depends(get_current_user),
) -> UserSafe:
    """Gets the current user (if active) according to the token."""
    print("get_current_active_user")
    if curr_usr.disabled:
        raise fa.HTTPException(status_code=400, detail="Inactive user")

    # Strip sensitive data before returning (e.g., password hash).
    curr_usr_safe = UserSafe(**curr_usr.dict())
    return curr_usr_safe


def authenticate_user(fake_db, username: str, password: str) -> Optional[User]:
    """Authenticates a user by checking its username and password."""
    user = get_user_by_username(fake_db, username)
    if not user:
        return None
    if not ut_pass.verify_password(password, user.hashed_password):
        return None
    return user
