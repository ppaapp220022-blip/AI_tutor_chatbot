from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette import status

from app.backend.database import get_db
from app.backend.model.users import Role
from app.backend.util.jwt_util import decode_token
from app.backend.repository.user_repository import find_user_id

bearer_schema = HTTPBearer()


# Header - Bearer
def get_current_users(token: HTTPAuthorizationCredentials = Depends(bearer_schema)) -> str:
    return decode_token(token.credentials)


# 관리자 권한 검증
def get_current_admin(
        login_id: str = Depends(get_current_users),
        db: Session = Depends(get_db)
) -> str:
    user = find_user_id(db, login_id)
    if not user or user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='관리자 권한이 없습니다'
        )
    return login_id
