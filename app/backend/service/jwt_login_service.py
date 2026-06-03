from loguru import logger
from sqlalchemy.orm import Session

from app.backend.database import redis_client
from app.backend.repository.user_repository import find_user_id
from app.backend.service.user_service import pwd_encoding
from app.backend.util.jwt_util import create_access_token, create_refresh_token
from app.backend.schema.users_schema import LoginRequest


def login(db: Session, user: LoginRequest) -> dict:
    """
    로그인
    :param db: 세션
    :param user: 로그인 요청
    :return: 엑세스 / 리프레시 토큰
    """
    logger.info(f'로그인 요청 : {user}')  # password 자동 제외
    exist_user = find_user_id(db, user.login_id)

    if not exist_user:
        raise ValueError('존재하지 않는 아이디입니다.')

    if not pwd_encoding.verify(user.password, exist_user.password):
        raise ValueError('비밀번호가 일치 하지 않습니다.')

    if not exist_user.is_active:
        raise ValueError('비활성화 된 아이디 입니다.')

    access_token = create_access_token(exist_user.login_id)
    refresh_token = create_refresh_token(exist_user.login_id)

    logger.info(f'로그인 완료 : {exist_user.login_id}')
    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}


def logout(login_id: str) -> None:
    """
    로그아웃
    :param login_id: 현재 로그인 된 아이디
    """
    redis_client.delete(f'refresh:{login_id}')
    logger.info(f'로그아웃 완료 : {login_id}')
