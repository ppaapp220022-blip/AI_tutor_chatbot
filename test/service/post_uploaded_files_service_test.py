from io import BytesIO
from pathlib import Path

from app.backend.service.uploaded_files_service import post_uploaded_files_service, save_upload_file_service
from app.backend.service.chat_room_service import post_chat_room_service
from app.backend.repository.user_repository import create_users

def test_post_uploaded_files_service(db):
    user = create_users(db, 'user1', '1234', 'user1@example.com')
    room = post_chat_room_service(db, user.id, 'test', 'test persona')

    file_name = 'test.pdf'
    file_path = r'C:\dev'
    upload = post_uploaded_files_service(db, room.id, file_name, file_path)

    assert upload.id is not None
    assert upload.room_id == room.id
    assert upload.file_name == 'test.pdf'
    assert upload.file_path == r'C:\dev'

class DummyUploadFile:
    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self.file = BytesIO(content)

def test_save_upload_file_service(db):
    user = create_users(db, 'user1', '1234', 'user1@example.com')
    room = post_chat_room_service(db, user.id, 'test', 'test persona')

    dummy_file = DummyUploadFile("test.pdf", b"%PDF-1.4 test content")

    saved = save_upload_file_service(db, room.id, dummy_file)

    assert saved.id is not None
    assert saved.room_id == room.id
    assert saved.file_name == "test.pdf"
    assert saved.file_path is not None
    assert Path(saved.file_path).exists()
