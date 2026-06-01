from io import BytesIO

import pytest

from app.backend.repository.messages_repository import list_messages_by_room
from app.backend.repository.uploaded_files_repository import list_uploaded_files
from app.backend.repository.user_repository import create_users
from app.backend.service.ai_chat_service import handle_chat_request_service
from app.backend.service.chat_room_service import post_chat_room_service


class DummyUploadFile:
    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self.file = BytesIO(content)


def test_handle_chat_request_service_without_real_pdf(db, monkeypatch):
    user = create_users(db, "user1", "1234", "user1@example.com")
    room = post_chat_room_service(db, user.id, "test", "test persona")

    dummy_file = DummyUploadFile("fake.pdf", b"not a real pdf")

    def fake_extract_text_from_file(file_path: str) -> str:
        return "이 문서는 파이썬 기초 문서입니다."

    def fake_request_chat_completion(messages: list[dict]) -> str:
        return "문서 요약 결과입니다."

    monkeypatch.setattr(
        "app.backend.service.ai_chat_service.extract_text_from_file",
        fake_extract_text_from_file,
    )
    monkeypatch.setattr(
        "app.backend.service.ai_chat_service.request_chat_completion",
        fake_request_chat_completion,
    )

    result = handle_chat_request_service(
        db,
        room.id,
        "이 문서를 요약해줘.",
        dummy_file,
    )

    assert result["room_id"] == room.id
    assert result["user_message"] == "이 문서를 요약해줘."
    assert result["uploaded_file_id"] is not None
    assert result["file_name"] == "fake.pdf"
    assert result["assistant_message"] == "문서 요약 결과입니다."
    messages = list_messages_by_room(db, room.id)
    assert len(messages) == 2


def test_handle_chat_request_service_rolls_back_when_ai_fails(db, monkeypatch, upload_dir):
    user = create_users(db, "user1", "1234", "user1@example.com")
    room = post_chat_room_service(db, user.id, "test", "test persona")

    dummy_file = DummyUploadFile("fake.pdf", b"not a real pdf")

    def fake_extract_text_from_file(file_path: str) -> str:
        return "이 문서는 파이썬 기초 문서입니다."

    def fake_request_chat_completion(messages: list[dict]) -> str:
        raise RuntimeError("openai failure")

    monkeypatch.setattr(
        "app.backend.service.ai_chat_service.extract_text_from_file",
        fake_extract_text_from_file,
    )
    monkeypatch.setattr(
        "app.backend.service.ai_chat_service.request_chat_completion",
        fake_request_chat_completion,
    )

    with pytest.raises(RuntimeError, match="openai failure"):
        handle_chat_request_service(
            db,
            room.id,
            "이 문서를 요약해줘.",
            dummy_file,
        )

    assert list_messages_by_room(db, room.id) == []
    assert list_uploaded_files(db, room.id) == []
    assert list(upload_dir.rglob("*")) == []
