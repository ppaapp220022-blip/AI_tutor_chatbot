from app.backend.repository.messages_repository import (
    create_messages,
    list_messages_by_room,
    find_messages,
    update_messages,
    delete_messages
)
from app.backend.model.messages import Role
from app.backend.repository.chat_room_repository import find_chat_room

# 메시지 생성
def post_messages_service(db, room_id: int, role: Role, content: str, commit: bool = True):

    if not room_id:
        raise ValueError("채팅방을 확인할 수 없습니다.")

    room = find_chat_room(db, room_id)
    if not room:
        raise ValueError("채팅방이 존재하지 않습니다.")

    messages = create_messages(db, room_id, role, content)

    if commit:
        db.commit()
        db.refresh(messages)

    return messages

# 메시지 목록
def get_all_messages_service(db, room_id: int):
    room = find_chat_room(db, room_id)
    if not room:
        raise ValueError("채팅방이 존재하지 않습니다.")

    messages = list_messages_by_room(db, room_id)

    return messages

# 메시지 단건 검색
def get_one_messages_service(db, message_id: int):
    messages = find_messages(db, message_id)

    if not messages:
        raise ValueError("메시지가 존재하지 않습니다.")

    return messages

# 메시지 수정
def patch_messages_service(db, messages_id: int, new_content: str):
    messages = update_messages(db, messages_id, new_content)

    if not messages:
        raise ValueError("수정할 메시지가 존재하지 않습니다.")

    db.commit()
    db.refresh(messages)
    return messages

# 메시지 삭제
def delete_messages_service(db, message_id: int):
    messages = find_messages(db, message_id)

    if not messages:
        raise ValueError("삭제할 메시지가 존재하지 않습니다.")

    delete_messages(db, message_id)
    db.commit()
    return True
