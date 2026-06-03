from app.backend.repository.chat_room_repository import (
    count_chat_rooms,
    create_chat_room,
    list_chat_rooms,
    find_chat_room,
    update_chat_room,
    delete_chat_room,
)
from app.backend.exception import BadRequestException, DatabaseException, NotFoundException
from app.backend.model.chat_room import ChatRoom
from app.backend.schema.base_schema import PaginationRequest
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# 채팅방 생성
def post_chat_room_service(db, member_id: int, title: str, persona: str):
    """
    채팅방 생성 서비스
    :param db: 세션
    :param member_id: 회원 FK
    :param title: 채팅방 제목
    :param persona: 페르소나
    :return: 생성된 채팅방
    """
    if not title or not title.strip():
        raise BadRequestException("채팅방 제목은 비어 있을 수 없습니다.")

    try:
        room = create_chat_room(db, member_id, title, persona)
        db.commit()
        db.refresh(room)
        return room
    except IntegrityError:
        db.rollback()
        raise BadRequestException("채팅방 생성에 필요한 회원 정보가 올바르지 않습니다.")
    except SQLAlchemyError:
        db.rollback()
        raise DatabaseException("채팅방 생성 중 데이터베이스 오류가 발생했습니다.")

# 채팅방 목록
def get_all_chat_room_service(db, pagination: PaginationRequest):
    """
    채팅방 목록 조회 서비스
    :param db: 세션
    :param pagination: 페이징 정보
    :return: 채팅방 목록
    """
    total = count_chat_rooms(db)
    items = list_chat_rooms(db, pagination.offset, pagination.size)
    return {
        "items": items,
        "total": total,
        "page": pagination.page,
        "size": pagination.size,
    }

# 채팅방 검색
def get_chat_room_service(db, room_id: int):
    """
    채팅방 단건 조회 서비스
    :param db: 세션
    :param room_id: 대화방 PK
    :return: 조회된 채팅방
    """
    room = find_chat_room(db, room_id)

    if not room:
        raise NotFoundException("채팅방이 존재하지 않습니다.")
    return room

# 채팅방 수정
def patch_chat_room_service(db, room_id: int, chat_room: ChatRoom):
    """
    채팅방 수정 서비스
    :param db: 세션
    :param room_id: 대화방 PK
    :param chat_room: 수정할 채팅방
    :return: 수정된 채팅방
    """
    try:
        room = update_chat_room(db, room_id, chat_room)

        if not room:
            raise NotFoundException("채팅방이 존재하지 않습니다.")

        db.commit()
        db.refresh(room)
        return room
    except NotFoundException:
        db.rollback()
        raise
    except SQLAlchemyError:
        db.rollback()
        raise DatabaseException("채팅방 수정 중 데이터베이스 오류가 발생했습니다.")

# 채팅방 삭제
def delete_chat_room_service(db, room_id: int):
    """
    채팅방 삭제 서비스
    :param db: 세션
    :param room_id: 대화방 PK
    :return: 삭제 여부
    """
    try:
        room = find_chat_room(db, room_id)

        if not room:
            raise NotFoundException("삭제할 채팅방이 없습니다.")

        delete_chat_room(db, room_id)
        db.commit()
        return True
    except NotFoundException:
        db.rollback()
        raise
    except SQLAlchemyError:
        db.rollback()
        raise DatabaseException("채팅방 삭제 중 데이터베이스 오류가 발생했습니다.")