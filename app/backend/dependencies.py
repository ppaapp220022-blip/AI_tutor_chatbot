from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.backend.util.jwt_util import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


# Header - Bearer
def get_current_users(token: str = Depends(oauth2_scheme)) -> str:
    return decode_token(token)
