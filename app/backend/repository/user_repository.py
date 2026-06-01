from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.backend.model.users import Users, Role
from loguru import logger


def create_users(db: Session, login_id: str, password: str, email: str) -> Users:
    """
    회원가입
    :param db: DB 세션 (DB 연결 통로 개념)
    :param login_id: 로그인 아이디
    :param password: 비밀번호
    :param email: 이메일
    :return: 회원
    """
    logger.info(f'회원 등록 요청 - 아이디 : {login_id}, 이메일 : {email}')
    user = Users(login_id=login_id, password=password, email=email, role=Role.USER)
    db.add(user)
    db.flush()
    db.refresh(user)
    logger.info(f'회원 등록 완료 - 아이디 : {user.login_id}, 이메일 : {user.email}')
    return user


def find_user(db: Session, login_id: str) -> Optional[Users]:
    """
    유저 단건 조회
    :param db: 세션
    :param login_id: 로그인 아이디
    :return: 회원
    """
    logger.info(f'유저 단건 조회 요청 : {login_id}')
    user = db.execute(select(Users).where(Users.login_id == login_id)).scalar_one_or_none()

    if not user:
        logger.warning(f'조회 유저 없음 : {login_id}')
        return None
    logger.info(f'유저 단건 조회 : {user.login_id}, {user.email}, {user.role}')

    return user


def update_user(db: Session, login_id: str, new_password: str, new_email: str) -> Optional[Users]:
    """
    회원 정보 업데이트
    :param db: DB 세션
    :param login_id: 로그인 아이디
    :param new_password: 변경할 비밀번호
    :param new_email: 변경할 이메일
    :return: 수정된 회원
    """
    logger.info(f'회원 정보 수정 요청 아이디 : {login_id}')
    user = find_user(db, login_id)

    if not user:
        logger.warning('지정 회원 존재 하지 않음')
        return None

    if new_password:
        user.password = new_password
    if new_email:
        user.email = new_email

    db.flush()
    db.refresh(user)

    logger.info(f'회원 정보 수정 : {user.login_id}, {user.email}')
    return user


def delete_user(db: Session, login_id: str) -> bool:
    """
    회원 삭제
    :param db: DB 세션
    :param login_id: 로그인 아이디
    :return: 삭제 여부
    """
    user = find_user(db, login_id)
    if not user:
        logger.warning('지정 회원 존재 하지 않음')
        return False
    db.delete(user)
    db.flush()
    logger.info(f'{login_id} 회원 삭제 완료')
    return True
