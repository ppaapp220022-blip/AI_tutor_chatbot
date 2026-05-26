from sqlalchemy.orm import Session
from app.backend.model.chat_room import ChatRoom
from loguru import logger


def create_chat_room(db: Session, member_id: int, title: str, persona: str) -> ChatRoom:
    """
    대화방 생성 함수
    :param db: 세션
    :param member_id: 회원 FK
    :param title: 대화방 제목
    :param persona: 페르소나
    :return: 대화방 생성
    """
    chat_room = ChatRoom(member_id = member_id, title = title, persona = persona)
    db.add(chat_room)
    db.commit()
    db.refresh(chat_room)
    logger.info(f'대화방 생성 : {chat_room.member_id}, {chat_room.title}, {chat_room.persona}')
    return chat_room


def find_chat_room(db: Session, chat_room_id: int) -> type[ChatRoom] | None:
    """
    채팅방 단건 조회
    :param db: 세션
    :param chat_room_id: 대화방 PK
    :return: 채팅방
    """
    logger.info(f'단건 조회 요청 : {chat_room_id}')
    chat_room = db.query(ChatRoom).filter(ChatRoom.id == chat_room_id).first()
    if not chat_room:
        logger.warning('조회 대화방 없음')
        return None
    logger.info(f'대화방 단건 조회 : {chat_room.member_id}, {chat_room.title}, {chat_room.persona}')

    return chat_room

def update_chat_room(db: Session, chat_room_id: int, chat_room: ChatRoom) -> type[ChatRoom] | None:
    logger.info(f'채팅방 수정 요청 - 제목 : {chat_room.title}, 페르소나 : {chat_room.persona}')
    room = find_chat_room(db, chat_room_id)

    if not room:
        logger.warning('수정할 채팅방 없음')
        return None

    if chat_room.title:
        room.title = chat_room.title
    if chat_room.persona:
        room.persona = chat_room.persona

    db.commit()
    db.refresh(room)
    logger.info(f'채팅방 수정 완료 - 제목 : {room.title}, 페르소나 : {room.persona}')
    return room

def delete_chat_room(db: Session, chat_room_id: int) -> type[ChatRoom] | None:
    room = find_chat_room(db, chat_room_id)
    if not room:
        logger.warning('삭제할 대화창 없음')
        return None
    db.delete(room)
    db.commit()
    logger.info(f'삭제 완료 - {room.member_id}, {room.title}, {room.persona}')
    return room
