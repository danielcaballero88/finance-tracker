import fastapi as fa
import fastapi.security as fas

import auth.util_password as util_password

oauth2_scheme = fas.OAuth2PasswordBearer(tokenUrl="token")
