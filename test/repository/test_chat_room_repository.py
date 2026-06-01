from app.backend.repository.chat_room_repository import create_chat_room, find_chat_room, update_chat_room, delete_chat_room
from app.backend.model.chat_room import ChatRoom
import pytest

def test_create_chat_room(db):
    member_id = 1
    title = 'test'
    persona = 'test persona'
    create_chat_room(db, member_id, title, persona)

    assert member_id is not None
    assert title == 'test'
    assert persona == 'test persona'

def test_find_chat_room(db):
    member_id = 1
    title = 'test'
    persona = 'test persona'
    room = create_chat_room(db, member_id, title, persona)

    find_chat_room(db, room.member_id)

def test_update_chat_room(db):
    member_id = 1
    title = 'test'
    persona = 'test persona'
    room = create_chat_room(db, member_id, title, persona)

    update_room = ChatRoom()
    update_room.title = 'test1'
    update_room.persona = 'test1 persona'
    update_chat_room(db, room.id, update_room)

def test_delete_chat_room(db):
    member_id = 1
    title = 'test'
    persona = 'test persona'
    room = create_chat_room(db, member_id, title, persona)
    delete_chat_room(db, room.id)
