import fastapi.security as fas

oauth2_scheme = fas.OAuth2PasswordBearer(tokenUrl="token")
