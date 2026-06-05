from loguru import logger
from sqlalchemy.orm import Session

from app.backend.database import redis_client
from app.backend.repository.user_repository import find_user_id
from app.backend.service.user_service import pwd_encoding
from app.backend.util.jwt_util import create_access_token, create_refresh_token, decode_token
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

    if not exist_user or not pwd_encoding.verify(user.password, exist_user.password):
        raise ValueError('아이디 또는 비밀번호가 틀렸습니다.')

    if not exist_user.is_active:
        raise ValueError('비활성화 된 아이디 입니다.')

    access_token = create_access_token(exist_user.login_id)
    refresh_token = create_refresh_token(exist_user.login_id)

    # 리프레시토큰 레디스에 저장
    redis_client.set(
        f'refresh:{exist_user.login_id}',
        refresh_token,
        ex=60 * 60 * 24,
    )

    logger.info(f'로그인 완료 : {exist_user.login_id}')
    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}


def refresh_access_token(refresh_token: str) -> dict:
    """
    리프레시 토큰으로 엑세스 토큰 재발급
    :param refresh_token: 리프레시 토큰
    :return: 새 엑세스 토큰
    """
    if not refresh_token:
        raise ValueError('리프레시 토큰이 없습니다.')

    login_id = decode_token(refresh_token, expected_type='refresh')
    saved_refresh_token = redis_client.get(f'refresh:{login_id}')
    if not saved_refresh_token or saved_refresh_token != refresh_token:
        raise ValueError('유효하지 않은 리프레시 토큰입니다.')

    access_token = create_access_token(login_id)
    logger.info(f'엑세스 토큰 재발급 완료 : {login_id}')
    return {'access_token': access_token, 'token_type': 'bearer'}


def logout(login_id: str) -> None:
    """
    로그아웃
    :param login_id: 현재 로그인 된 아이디
    """
    redis_client.delete(f'refresh:{login_id}')
    logger.info(f'로그아웃 완료 : {login_id}')
