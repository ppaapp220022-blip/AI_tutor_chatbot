from app.backend.repository.messages_repository import (
    count_messages_by_room,
    create_messages,
    list_messages_by_room,
    list_recent_messages_by_room,
    find_messages,
    update_messages,
    delete_messages
)
from app.backend.exception import BadRequestException, DatabaseException, NotFoundException
from app.backend.model.messages import Role
from app.backend.repository.chat_room_repository import find_chat_room
from app.backend.schema.base_schema import PaginationRequest
from sqlalchemy.exc import SQLAlchemyError

# 메시지 생성
def post_messages_service(db, room_id: int, role: Role, content: str, commit: bool = True):
    """
    메시지 생성 서비스
    :param db: 세션
    :param room_id: 대화방 PK
    :param role: 메시지 역할
    :param content: 메시지 내용
    :param commit: 커밋 여부
    :return: 생성된 메시지
    """
    if not room_id:
        raise BadRequestException("채팅방을 확인할 수 없습니다.")

    room = find_chat_room(db, room_id)
    if not room:
        raise NotFoundException("채팅방이 존재하지 않습니다.")

    try:
        messages = create_messages(db, room_id, role, content)

        if commit:
            db.commit()
            db.refresh(messages)

        return messages
    except SQLAlchemyError:
        db.rollback()
        raise DatabaseException("메시지 저장 중 데이터베이스 오류가 발생했습니다.")

# 메시지 목록
def get_all_messages_service(db, room_id: int, pagination: PaginationRequest):
    """
    메시지 목록 조회 서비스
    :param db: 세션
    :param room_id: 대화방 PK
    :param pagination: 페이징 정보
    :return: 메시지 목록
    """
    room = find_chat_room(db, room_id)
    if not room:
        raise NotFoundException("채팅방이 존재하지 않습니다.")

    total = count_messages_by_room(db, room_id)
    items = list_messages_by_room(db, room_id, pagination.offset, pagination.size)

    return {
        "items": items,
        "total": total,
        "page": pagination.page,
        "size": pagination.size,
    }

def get_message_history_service(db, room_id: int, limit: int = 20):
    """
    AI 채팅용 최근 메시지 이력 조회 서비스
    :param db: 세션
    :param room_id: 대화방 PK
    :param limit: 조회할 최근 메시지 수
    :return: 최근 메시지 목록
    """
    room = find_chat_room(db, room_id)
    if not room:
        raise NotFoundException("채팅방이 존재하지 않습니다.")

    return list_recent_messages_by_room(db, room_id, limit)

# 메시지 단건 검색
def get_one_messages_service(db, message_id: int):
    """
    메시지 단건 조회 서비스
    :param db: 세션
    :param message_id: 메시지 PK
    :return: 조회된 메시지
    """
    messages = find_messages(db, message_id)

    if not messages:
        raise NotFoundException("메시지가 존재하지 않습니다.")

    return messages

# 메시지 수정
def patch_messages_service(db, messages_id: int, new_content: str):
    """
    메시지 수정 서비스
    :param db: 세션
    :param messages_id: 메시지 PK
    :param new_content: 수정할 메시지 내용
    :return: 수정된 메시지
    """
    try:
        messages = update_messages(db, messages_id, new_content)

        if not messages:
            raise NotFoundException("수정할 메시지가 존재하지 않습니다.")

        db.commit()
        db.refresh(messages)
        return messages
    except NotFoundException:
        db.rollback()
        raise
    except SQLAlchemyError:
        db.rollback()
        raise DatabaseException("메시지 수정 중 데이터베이스 오류가 발생했습니다.")

# 메시지 삭제
def delete_messages_service(db, message_id: int):
    """
    메시지 삭제 서비스
    :param db: 세션
    :param message_id: 메시지 PK
    :return: 삭제 여부
    """
    try:
        messages = find_messages(db, message_id)

        if not messages:
            raise NotFoundException("삭제할 메시지가 존재하지 않습니다.")

        delete_messages(db, message_id)
        db.commit()
        return True
    except NotFoundException:
        db.rollback()
        raise
    except SQLAlchemyError:
        db.rollback()
        raise DatabaseException("메시지 삭제 중 데이터베이스 오류가 발생했습니다.")