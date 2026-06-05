from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.backend.util.jwt_util import decode_token

bearer_schema = HTTPBearer()

# Header - Bearer
def get_current_users(token: HTTPAuthorizationCredentials = Depends(bearer_schema)) -> str:
    return decode_token(token.credentials)
