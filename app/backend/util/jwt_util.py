from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Depends
from jose import jwt, JWTError
from loguru import logger
import os

load_dotenv()

JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY') or ''
JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM') or 'HS256'
JWT_ACCESS_EXPIRE_MINUTES: int = int(os.getenv('JWT_ACCESS_EXPIRE_MINUTES') or '30')
JWT_REFRESH_EXPIRE_DAYS: int = int(os.getenv('JWT_REFRESH_EXPIRE_DAYS') or '7')

if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY 환경변수가 설정되지 않았습니다")


def create_access_token(login_id: str) -> str:
    """
    엑세스 토큰 발급
    :param login_id: 회원 아이디
    :return: 엑세스토큰
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_ACCESS_EXPIRE_MINUTES)
    date = {"sub": login_id, "type": "access", "exp": expire}
    token = jwt.encode(date, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    logger.info(f'엑세스 토큰 생성 : {login_id}, {token}')
    return token


def create_refresh_token(login_id: str) -> str:
    """
    리프레시 토큰 발급
    :param login_id: 회원 아이디
    :return: 리프레시토큰
    """
    expire = datetime.now(timezone.utc) + timedelta(days=JWT_REFRESH_EXPIRE_DAYS)
    date = {"sub": login_id, "type": "refresh", "exp": expire}
    token = jwt.encode(date, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    logger.info(f'리프레시 토큰 생성 : {login_id}, {token}')
    return token


def decode_token(token: str) -> str:
    """
    토큰 검증
    :param token: JWT 토큰
    :return: 로그인 아이디
    """
    try:
        payload: dict = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        login_id: str = payload.get("sub") or ''
        if not login_id:
            raise ValueError('유효하지 않은 토큰입니다.')
        return login_id
    except JWTError:
        logger.warning('토큰 디코드 실패')
        raise ValueError('유효하지 않는 토큰입니다.')