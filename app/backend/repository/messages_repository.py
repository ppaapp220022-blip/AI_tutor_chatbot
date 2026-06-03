from sqlalchemy import func
from sqlalchemy.orm import Session
from app.backend.model.messages import Messages, Role
from loguru import logger

def create_messages(db: Session, room_id: int, role: Role, content: str) -> Messages:
    """
    메시지 생성
    :param db: DB 세션
    :param room_id: 대화방 번호
    :param role: 발화 주체(user/assistant)
    :param content: 메시지 내용
    :return: 생성된 메시지
    """
    logger.info(f"메시지 생성 요청 - room_id: {room_id}, role: {role}, content: {content}")
    messages = Messages(room_id=room_id, role=role, content=content)
    db.add(messages)
    db.flush()
    db.refresh(messages)
    logger.info(f"메시지 생성 완료 - id: {messages.id}, room_id: {messages.room_id}")
    return messages

def list_messages_by_room(db: Session, room_id: int, offset: int, limit: int) -> list[Messages]:
    """
    대화방별 메시지 목록 조회
    :param db: DB 세션
    :param room_id: 대화방 번호
    :param offset: 조회 시작 위치
    :param limit: 조회 건수
    :return: 메시지 목록
    """
    logger.info(f"메시지 목록 조회 요청 - room_id: {room_id}")
    messages = (
        db.query(Messages)
        .filter(Messages.room_id == room_id)
        .order_by(Messages.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    logger.info(f"메시지 목록 조회 완료 - room_id: {room_id}, count: {len(messages)}")
    return messages

def list_recent_messages_by_room(db: Session, room_id: int, limit: int) -> list[Messages]:
    """
    대화방별 최근 메시지 목록 조회
    :param db: DB 세션
    :param room_id: 대화방 번호
    :param limit: 조회 건수
    :return: 최근 메시지 목록
    """
    logger.info(f"최근 메시지 목록 조회 요청 - room_id: {room_id}, limit: {limit}")
    messages = (
        db.query(Messages)
        .filter(Messages.room_id == room_id)
        .order_by(Messages.id.desc())
        .limit(limit)
        .all()
    )
    messages.reverse()
    logger.info(f"최근 메시지 목록 조회 완료 - room_id: {room_id}, count: {len(messages)}")
    return messages

def count_messages_by_room(db: Session, room_id: int) -> int:
    """
    대화방별 메시지 전체 건수 카운트(페이징)
    :param db: DB 세션
    :param room_id: 대화방 번호
    :return: 메시지 전체 건수
    """
    return db.query(func.count(Messages.id)).filter(Messages.room_id == room_id).scalar() or 0

def find_messages(db: Session, messages_id: int) -> Messages | None:
    """
    메시지 단건 조회
    :param db: DB 세션
    :param messages_id: 메시지 번호
    :return: 메시지
    """
    logger.info(f"메시지 단건 조회 요청 - messages_id: {messages_id}")
    messages = db.query(Messages).filter(Messages.id == messages_id).first()

    if not messages:
        logger.warning(f"메시지가 조회되지 않습니다. message_id: {messages_id}")
        return None

    logger.info(f"메시지 단건 조회 완료 - id: {messages.id}, room_id: {messages.room_id}")
    return messages

def update_messages(db: Session, messages_id: int, new_content: str) -> Messages | None:
    """
    메시지 내용 수정
    :param db: DB 세션
    :param messages_id: 메시지 번호
    :param new_content: 변경할 내용
    :return: 변경된 메시지
    """
    logger.info(f"메시지 수정 요청 - message_id: {messages_id}")
    messages = find_messages(db, messages_id)

    if not messages:
        logger.warning(f"수정할 메시지가 없습니다. message_id: {messages_id}")
        return None

    if new_content:
        messages.content = new_content

    db.flush()
    db.refresh(messages)
    logger.info(f"메시지 수정 완료 - id: {messages.id}, content: {messages.content}")
    return messages

def delete_messages(db: Session, messages_id: int) -> bool:
    """
    메시지 삭제
    :param db: DB 세션
    :param messages_id: 메시지 번호
    :return: 삭제 성공 여부
    """
    logger.info(f"메시지 삭제 요청 - message_id: {messages_id}")
    message = find_messages(db, messages_id)

    if not message:
        logger.warning(f"삭제할 메시지가 없습니다. message_id: {messages_id}")
        return False

    db.delete(message)
    db.flush()
    logger.info(f"메시지 삭제 완료 - message_id: {messages_id}")
    return True