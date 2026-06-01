from app.backend.repository.chat_room_repository import create_chat_room, find_chat_room, update_chat_room, delete_chat_room
from app.backend.model.chat_room import ChatRoom
from app.backend.repository.user_repository import create_users
import pytest

def test_create_chat_room(db):
    user = create_users(db, 1, 1234, 'test@test.com')
    title = 'test'
    persona = 'test persona'
    title = 'test'
    persona = 'test persona'
    create_chat_room(db, user.id, title, persona)
    assert user is not None
    assert title == 'test'
    assert persona == 'test persona'

def test_find_chat_room(db):
    user = create_users(db, 2, 1234, 'test@test.com')
    title = 'test'
    persona = 'test persona'
    room = create_chat_room(db, user.id, title, persona)
    find_chat_room(db, room.member_id)

def test_update_chat_room(db):
    user = create_users(db, 3, 1234, 'test@test.com')
    title = 'test'
    persona = 'test persona'
    room = create_chat_room(db, user.id, title, persona)

    update_room = ChatRoom()
    update_room.title = 'test1'
    update_room.persona = 'test1 persona'
    update_chat_room(db, room.id, update_room)

def test_delete_chat_room(db):
    user = create_users(db, 4, 1234, 'test@test.com')
    title = 'test'
    persona = 'test persona'
    room = create_chat_room(db, user.id, title, persona)
    delete_chat_room(db, room.id)