"""Authentication Package.

This subpackage is meant to provide all the authentication functionality
for the API (user registration and login).
To do this, it implements the username/password flow using OAuth2.
"""

import fastapi as fa
import fastapi.security as fas

import auth.models.user as u
import auth.utils.password as p
import auth.utils.token as t

oauth2_scheme = fas.OAuth2PasswordBearer(tokenUrl="token")


def register_new_user(new_user: u.UserRegister):
    """Registers a new user.

    The new user must be a `UserAdd` object with a unique `username`
    because it is used as the MongoDB `id_`.
    """
    # Parse new user data.
    username = new_user.username
    email = new_user.email
    password = new_user.password
    disabled = False
    hashed_password = p.get_password_hash(password)

    # Assemble new user dictionary and convert to pydantic object.
    new_user_dict = {
        "username": username,
        "email": email,
        "disabled": disabled,
        "hashed_password": hashed_password,
    }
    new_user_db = u.UserDB(**new_user_dict)

    # Add to the DB.
    result = new_user_db.add()

    # Get the MongoDB id_ and return.
    result_id = str(result.inserted_id)
    return result_id


def get_current_user(
    token: str = fa.Depends(oauth2_scheme),
) -> u.UserBase:
    """Gets the current user from the DB according to the bearer token.

    The token contains the `username` under the key "sub", and that is
    used as the MongoDB `id_` in the "user" collection, so the matching
    user object is fetched.
    """
    # Decode token.
    token_data = t.decode_token(token)

    # Get user.
    user_db = u.UserDB.get(username=token_data.username)

    if user_db.disabled:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_401_UNAUTHORIZED, detail="Inactive user"
        )

    # Filter out sensitive data and return.
    user = u.UserBase(**user_db.dict())
    return user


def authenticate_user(username: str, password: str) -> t.Token:
    """Authenticates a user by checking its username and password.

    If the authentication is successful a bearer token is returned for
    the user. Otherwise a "401 Unauthorized" is returned.

    Args:
        username (str): The user to authenticate.
        password (str): The password given for authentication.

    Returns:
        token (Token): Token object.

    Raises:
        HTTPException "401 Unauthorized": If the provided credentials
            are not correct.
    """
    # Get the user data from the DB.
    user_db = u.UserDB.get(username=username)

    # Check if the password is correct.
    if not p.verify_password(password, user_db.hashed_password):
        raise fa.HTTPException(
            status_code=fa.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username and/or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Parse into pydantic object for validation.
    user = u.UserBase(**user_db.dict())

    # Create new access token for the user.
    token = t.create_access_token(user.username)

    # Done.
    return token
