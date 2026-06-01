from typing import Optional
import random

from passlib.context import CryptContext
from app.backend.model import Users
from sqlalchemy.orm import Session
from app.backend.repository.user_repository import (
    create_users, find_user_id, update_user, update_users_active, find_users_by_ids_and_active
)
from app.backend.schema.users_schema import UserRequest, UserResponse, UsersActiveRequest
from app.backend.database import redis_client
from app.backend.util.email_utils import send_email
from loguru import logger

# 암호화
pwd_encoding = CryptContext(schemes=["bcrypt"])

# OTP 제한시간 3분
EXPIRED_OTP = 60 * 3


def add_user(db: Session, user: UserRequest) -> Optional[UserResponse]:
    """
    회원가입
    :param db: 세션
    :param user: 유저 정보
    :return: 회원
    """
    logger.info(f'회원가입 요청 : {user}')  # password 자동 제외
    exist_user = find_user_id(db, user.login_id)
    if exist_user:
        raise ValueError('이미 존재 하는 아이디 입니다.')

    password = pwd_encoding.hash(user.password)
    model_user = Users(login_id=user.login_id, password=password, email=user.email)
    created_user = create_users(db, model_user)
    logger.info(f'회원가입 완료 : {UserResponse.model_validate(created_user)}')
    return UserResponse.model_validate(created_user)


def send_otp_code(email: str):
    """
    OTP 메일 발송
    :param email: 보낼 이메일
    """
    otp = str(random.randint(100000, 999999))
    redis_client.setex(f'verify : {email}', EXPIRED_OTP, otp)
    logger.info(f'OTP Redis Save : {otp}')
    send_email(email, otp)


def vacillation_otp(email: str, otp: str) -> bool:
    """
    OTP 검증
    :param email: 검증할 이메일
    :param otp: OTP
    :return: 검증 여부
    """
    saved_otp = redis_client.get(f'verify : {email}')

    if not saved_otp:
        logger.warning(f'OTP 만료 혹은 없음 : {email}')
        raise ValueError('OTP 만료가 되었거나 일치하는 코드 없음')

    if saved_otp != otp:
        logger.warning(f'OTP 불일치 : {email}')
        raise ValueError('OTP가 일치 하지 않습니다.')

    redis_client.delete(f'verify : {email}')
    logger.info(f'OTP 인증 완료 : {email}')
    return True


def modify_user(db: Session, user: UserRequest) -> Optional[UserResponse]:
    """
    회원 정보 수정
    :param db: 세션
    :param user: 수정 유저 정보
    :return: 수정된 유저 정보
    """
    logger.info(f'회원 정보 수정 요청 : {user}')  # password 자동 제외
    exist_user = find_user_id(db, user.login_id)
    if not exist_user:
        logger.warning(f'존재하지 않는 회원 : {user.login_id}')
        raise ValueError(f'없는 회원 수정불가 : {user.login_id}')

    if pwd_encoding.verify(user.password, exist_user.password):
        logger.warning(f'현재 비밀번호와 겹침 : {user.login_id}')
        raise ValueError('현재 비밀번호랑 겹침 변경 불가')

    if exist_user.email == user.email:
        logger.warning(f'현재 이메일과 동일 : {user.email}')
        raise ValueError('현재 이메일과 동일함 변경 불가')

    new_password = pwd_encoding.hash(user.password)
    updated = update_user(db, user.login_id, new_password, user.email)
    logger.info(f'회원 정보 수정 완료 : {UserResponse.model_validate(updated)}')
    return UserResponse.model_validate(updated)


def modify_active_user(db: Session, user: UsersActiveRequest) -> int:
    """
    회원 상태 변경 (이미 같은 상태인 회원 스킵)
    :param db: 세션
    :param user: 변경할 회원과 상태
    :return: 변경된 회원수
    """
    logger.info(f'회원 상태 변경 요청 : {user}')
    target_users = find_users_by_ids_and_active(db, user.user_idx, user.is_active)

    if not target_users:
        logger.warning('모든 회원이 이미 동일한 상태입니다')
        raise ValueError('모든 회원이 이미 동일한 상태입니다')

    target_ids = [u.id for u in target_users]
    count = update_users_active(db, target_ids, user.is_active)
    logger.info(f'활성화 상태 변경 완료 - {count}명')
    return count
