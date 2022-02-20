import fastapi as fa
import fastapi.security as fas

import auth
import auth.models.user as u
import mongodb

app = fa.FastAPI()


@app.on_event("startup")
async def startup():
    mongodb.mongo_conn.open_client()


@app.on_event("shutdown")
async def shutdown():
    mongodb.mongo_conn.close_client()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/register")
async def register(new_user: u.UserRegister):
    """Registers a new user."""
    new_user_id = auth.register_new_user(new_user)
    return {"id_": new_user_id}


@app.post("/login")
async def login(form_data: fas.OAuth2PasswordRequestForm = fa.Depends()):
    """Logins a user (using username and password) and returns a token."""
    token = auth.authenticate_user(form_data.username, form_data.password)
    return token


@app.get("/users/me")
async def get_users_me(
    me: u.UserBase = fa.Depends(auth.get_current_user),
):
    """Get the user making the request.

    GET /users/me gets the data of the user associated with the bearer
    token passed for authentication in the headers.

    Dependency injection:
    - u.get_current_active_user(UserBase) -> UserBase
        - u.get_current_user(token) -> UserBase
    """
    return me
