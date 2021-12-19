from typing import Optional

import fastapi as fa
import fastapi.security as fa_s

import auth
import models.user as u

app = fa.FastAPI()


@app.get("/")
async def read_root(token: str = fa.Depends(auth.shared.oauth2_scheme)):
    return {"Hello": "World"}


@app.post("/register")
async def register_new_user(usr: u.User):
    return usr


@app.post("/token")
async def login(form_data: fa_s.OAuth2PasswordRequestForm = fa.Depends()):
    # Get user data by username from the DB.
    user_dict = u.FAKE_USERS_DB.get(form_data.username)
    if not user_dict:
        raise fa.HTTPException(
            status_code=400,
            detail="Wrong username or password",
        )
    user = u.UserInDB(**user_dict)

    # Check if the entered password is correct.
    hashed_password = u.fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise fa.HTTPException(
            status_code=400,
            detail="Wrong username or password",
        )

    # Create token and return.
    acces_token = u.fake_create_token(user)
    return {"access_token": acces_token, "token_type": "bearer"}


@app.get("/users/me")
async def get_users_me(me: Optional[u.User] = fa.Depends(u.get_current_active_user)):
    """Get the user making the request.

    GET /users/me gets the data of the user associated with the bearer
    token passed for authentication in the headers.

    Dependency injection:
    - u.get_current_active_user(User) -> User | raise HTTPException
        - u.get_current_user(token) -> User
    """
    print("get_users_me")
    return me
