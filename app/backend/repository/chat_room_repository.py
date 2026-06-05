from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.backend.model.chat_room import ChatRoom
from loguru import logger

def create_chat_room(db: Session, member_id: int, title: str, persona: str) -> ChatRoom:
    """
    대화방 생성
    :param db: 세션
    :param member_id: 회원 FK
    :param title: 대화방 제목
    :param persona: 페르소나
    :return: 생성된 대화방
    """
    logger.info(f'대화방 생성 요청 - 회원 : {member_id}, 제목 : {title}')
    chat_room = ChatRoom(member_id=member_id, title=title, persona=persona)
    db.add(chat_room)
    db.flush()
    db.refresh(chat_room)
    logger.info(f'대화방 생성 완료 : {chat_room.member_id}, {chat_room.title}, {chat_room.persona}')
    return chat_room

def find_chat_room(db: Session, chat_room_id: int, login_id: str | None = None) -> Optional[ChatRoom]:
    """
    채팅방 단건 조회
    :param db: 세션
    :param chat_room_id: 대화방 PK
    :param login_id: 로그인 아이디
    :return: 채팅방
    """
    logger.info(f'단건 조회 요청 : room_id={chat_room_id}, login_id={login_id}')
    query = select(ChatRoom).where(ChatRoom.id == chat_room_id)
    if login_id:
        query = query.join(ChatRoom.users).where(ChatRoom.users.has(login_id=login_id))
    chat_room = db.execute(query).scalar_one_or_none()

    if not chat_room:
        logger.warning('조회 대화방 없음')
        return None

    logger.info(f'대화방 단건 조회 : {chat_room.member_id}, {chat_room.title}, {chat_room.persona}')
    return chat_room

def list_chat_rooms(db: Session, offset: int, limit: int, login_id: str | None = None) -> list[ChatRoom]:
    """
    채팅방 목록 조회
    :param db: 세션
    :param offset: 조회 시작 위치
    :param limit: 조회 건수
    :param login_id: 로그인 아이디
    :return: 채팅방 목록
    """
    logger.info(f'채팅방 목록 조회 요청 : login_id={login_id}')
    query = select(ChatRoom).order_by(ChatRoom.id.asc()).offset(offset).limit(limit)
    if login_id:
        query = (
            select(ChatRoom)
            .join(ChatRoom.users)
            .where(ChatRoom.users.has(login_id=login_id))
            .order_by(ChatRoom.id.asc())
            .offset(offset)
            .limit(limit)
        )
    chat_rooms = db.execute(query).scalars().all()
    logger.info(f'채팅방 목록 조회 완료 - login_id={login_id}, count: {len(chat_rooms)}')
    return list(chat_rooms)

def count_chat_rooms(db: Session, login_id: str | None = None) -> int:
    """
    채팅방 전체 건수 카운트(페이징)
    :param db: 세션
    :param login_id: 로그인 아이디
    :return: 전체 건수
    """
    query = select(func.count()).select_from(ChatRoom)
    if login_id:
        query = (
            select(func.count(ChatRoom.id))
            .join(ChatRoom.users)
            .where(ChatRoom.users.has(login_id=login_id))
        )
    return db.execute(query).scalar_one()

def update_chat_room(db: Session, chat_room_id: int, chat_room: ChatRoom) -> Optional[ChatRoom]:
    """
    채팅방 수정
    :param db: 세션
    :param chat_room_id: 대화방 PK
    :param chat_room: 수정할 대화방 데이터
    :return: 수정된 대화방
    """
    logger.info(f'채팅방 수정 요청 - 제목 : {chat_room.title}, 페르소나 : {chat_room.persona}')
    room = find_chat_room(db, chat_room_id)

    if not room:
        logger.warning('수정할 채팅방 없음')
        return None

    if chat_room.title:
        room.title = chat_room.title
    if chat_room.persona:
        room.persona = chat_room.persona

    db.flush()
    db.refresh(room)
    logger.info(f'채팅방 수정 완료 - 제목 : {room.title}, 페르소나 : {room.persona}')
    return room

def delete_chat_room(db: Session, chat_room_id: int) -> bool:
    """
    채팅방 삭제
    :param db: 세션
    :param chat_room_id: 대화방 PK
    :return: 삭제 여부
    """
    room = find_chat_room(db, chat_room_id)
    if not room:
        logger.warning('삭제할 대화방 없음')
        return False
    db.delete(room)
    db.flush()
    logger.info(f'삭제 완료 - {room.member_id}, {room.title}, {room.persona}')
    return True