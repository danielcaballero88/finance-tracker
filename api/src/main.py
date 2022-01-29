from datetime import timedelta
from typing import Optional

import fastapi as fa
import fastapi.security as fa_s

import auth
import auth.util_password as ut_passwd
import auth.util_token as ut_token
import models.user as u

app = fa.FastAPI()


@app.get("/")
async def read_root(token: str = fa.Depends(auth.oauth2_scheme)):
    return {"Hello": "World"}


@app.post("/register")
async def register_new_user(new_user_data: u.UserCreate) -> u.User:
    username = new_user_data.username
    email = new_user_data.email
    password = new_user_data.password
    disabled = False
    hashed_password = ut_passwd.get_password_hash(password)
    if username in u.FAKE_USERS_DB:
        u.FAKE_USERS_DB.pop(username)
    new_user = {
        "username": username,
        "email": email,
        "disabled": disabled,
        "hashed_password": hashed_password,
    }
    u.FAKE_USERS_DB[username] = new_user
    new_user = u.User(**new_user)
    return new_user


@app.post("/token", response_model=ut_token.Token)
async def login(form_data: fa_s.OAuth2PasswordRequestForm = fa.Depends()):
    """Logins a user (using username and password) and returns a token."""
    user = u.authenticate_user(u.FAKE_USERS_DB, form_data.username, form_data.password)

    if not user:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = ut_token.create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def get_users_me(
    me: Optional[u.UserSafe] = fa.Depends(u.get_current_active_user),
):
    """Get the user making the request.

    GET /users/me gets the data of the user associated with the bearer
    token passed for authentication in the headers.

    Dependency injection:
    - u.get_current_active_user(User) -> User | raise HTTPException
        - u.get_current_user(token) -> User
    """
    print("get_users_me")
    return me
