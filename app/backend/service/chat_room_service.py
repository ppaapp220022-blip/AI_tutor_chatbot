from app.backend.repository.chat_room_repository import (
    create_chat_room,
    find_chat_room,
    update_chat_room,
    delete_chat_room,
)
from app.backend.model.chat_room import ChatRoom

# 채팅방 생성
def post_chat_room_service(db, member_id: int, title: str, persona: str):

    if not title or not title.strip():
        raise ValueError("채팅방 제목은 비어 있을 수 없습니다.")

    room = create_chat_room(db, member_id, title, persona)
    db.commit()
    db.refresh(room)

    return room

# 채팅방 검색
def get_chat_room_service(db, room_id: int):
    room = find_chat_room(db, room_id)

    if not room:
        raise ValueError("채팅방이 존재하지 않습니다.")

    return room

# 채팅방 수정
def patch_chat_room_service(db, room_id: int, chat_room: ChatRoom):
    room = update_chat_room(db, room_id, chat_room)

    if not room:
        raise ValueError("채팅방이 존재하지 않습니다.")

    db.commit()
    db.refresh(room)
    return room

# 채팅방 삭제
def delete_chat_room_service(db, room_id: int):
    room = find_chat_room(db, room_id)

    if not room:
        raise ValueError("삭제할 채팅방이 없습니다.")

    delete_chat_room(db, room_id)
    db.commit()
    return True
