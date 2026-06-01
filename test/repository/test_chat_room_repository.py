from app.backend.repository.chat_room_repository import create_chat_room, find_chat_room, update_chat_room, delete_chat_room
from app.backend.model.chat_room import ChatRoom
from app.backend.repository.user_repository import create_users

def test_create_chat_room(db):
    user = create_users(db, 'user', '1234', 'user@example.com')
    title = 'test'
    persona = 'test persona'
    room = create_chat_room(db, user.id, title, persona)

    assert room.id is not None
    assert room.member_id == user.id
    assert room.title == 'test'
    assert room.persona == 'test persona'

def test_find_chat_room(db):
    user = create_users(db, 'user', '1234', 'user@example.com')
    title = 'test'
    persona = 'test persona'
    room = create_chat_room(db, user.id, title, persona)

    found = find_chat_room(db, room.id)
    assert found is not None
    assert found.id == room.id

def test_update_chat_room(db):
    user = create_users(db, 'user', '1234', 'user@example.com')
    title = 'test'
    persona = 'test persona'
    room = create_chat_room(db, user.id, title, persona)

    update_room = ChatRoom()
    update_room.title = 'test1'
    update_room.persona = 'test1 persona'
    updated = update_chat_room(db, room.id, update_room)
    assert updated.title == 'test1'
    assert updated.persona == 'test1 persona'

def test_delete_chat_room(db):
    user = create_users(db, 'user', '1234', 'user@example.com')
    title = 'test'
    persona = 'test persona'
    room = create_chat_room(db, user.id, title, persona)
    assert delete_chat_room(db, room.id) is True
    assert find_chat_room(db, room.id) is None
