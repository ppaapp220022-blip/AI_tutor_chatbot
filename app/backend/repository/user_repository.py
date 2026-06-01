from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from app.backend.model.users import Users, Role
from loguru import logger


def create_users(db: Session, user: Users) -> Users:
    """
    회원가입
    :param db: DB 세션
    :param user: 회원 정보
    :return: 회원
    """
    logger.info(f'회원 등록 요청 : {user}')
    user = Users(login_id=user.login_id, password=user.password, email=user.email, role=Role.USER)
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f'회원 등록 완료 : {user}')
    return user


def find_user_id(db: Session, login_id: str) -> Optional[Users]:
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
    logger.info(f'유저 단건 조회 완료 : {user}')
    return user


def find_users_by_ids_and_active(db: Session, user_ids: list[int], is_active: bool) -> list[Users]:
    """
    PK 목록 중 변경이 필요한 회원만 조회
    :param db: 세션
    :param user_ids: 회원 PK 목록
    :param is_active: 변경할 활성화 여부
    :return: 변경 대상 회원 목록
    """
    users = db.execute(
        select(Users)
        .where(Users.id.in_(user_ids))
        .where(Users.is_active != is_active)
    ).scalars().all()
    logger.info(f'변경 대상 회원 조회 완료 : {len(users)}명 → {[str(u) for u in users]}')
    return list(users)


def update_user(db: Session, login_id: str, password: str, email: str) -> Optional[Users]:
    """
    회원 정보 업데이트 (DB 작업만)
    :param db: DB 세션
    :param login_id: 로그인 아이디
    :param password: 변경할 비밀번호
    :param email: 변경할 이메일
    :return: 수정된 회원
    """
    logger.info(f'회원 정보 수정 요청 아이디 : {login_id}')
    user = find_user_id(db, login_id)

    if not user:
        logger.warning('지정 회원 존재 하지 않음')
        return None

    user.password = password
    user.email = email
    db.commit()
    db.refresh(user)
    logger.info(f'회원 정보 수정 완료 : {user}')
    return user


def update_users_active(db: Session, user_ids: list[int], is_active: bool) -> int:
    """
    단건 / 여러건 상태 변경
    :param db: 세션
    :param user_ids: 변경할 PK 목록
    :param is_active: 계정 활성화 여부
    :return: 변경된 회원 수
    """
    count = len(user_ids)
    db.execute(update(Users).where(Users.id.in_(user_ids)).values(is_active=is_active))
    db.commit()
    logger.info(f'활성화 여부 변경 완료 : ids={user_ids}, is_active={is_active}, count={count}')
    return count


def delete_user(db: Session, login_id: str) -> bool:
    """
    회원 삭제
    :param db: DB 세션
    :param login_id: 로그인 아이디
    :return: 삭제 여부
    """
    user = find_user_id(db, login_id)
    if not user:
        logger.warning('지정 회원 존재 하지 않음')
        return False
    db.delete(user)
    db.commit()
    logger.info(f'회원 삭제 완료 : {user}')
    return True
