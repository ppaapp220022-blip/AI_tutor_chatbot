from typing import Any

from app.frontend.api.http_client import request_api

ROOM_PAGE_SIZE = 5
MESSAGE_PAGE_SIZE = 5


def _request_api(
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    files: dict[str, Any] | None = None,
) -> Any:
    # 공통 HTTP 요청을 보내고 네트워크/상태 코드 오류를 일관되게 처리
    return request_api(
        method,
        path,
        params=params,
        json=json,
        data=data,
        files=files,
    )


def _normalize_role(role: Any) -> str:
    # 백엔드 role 값을 Streamlit chat_message 형식에 맞게 변환한다.
    """Convert backend message role values into Streamlit chat roles."""
    if isinstance(role, dict):
        role = role.get("value")
    if hasattr(role, "value"):
        role = role.value
    role_text = str(role).lower()
    return "assistant" if role_text == "assistant" else "user"


def _normalize_room(room: dict[str, Any]) -> dict[str, Any]:
    # 채팅방 응답을 프론트에서 쓰는 필드 구조로 정리한다.
    """Convert raw room payloads into the room shape used by the chat UI."""
    return {
        "id": room["id"],
        "member_id": room.get("member_id"),
        "title": room.get("title") or "제목 없는 채팅방",
        "persona": room.get("persona") or "",
        "created_at": room.get("created_at"),
    }


def _normalize_message(message: dict[str, Any]) -> dict[str, Any]:
    # 메시지 응답을 프론트에서 바로 렌더링할 수 있는 형태로 정리한다.
    """Convert raw message payloads into the message shape used by the chat UI."""
    return {
        "id": message.get("id"),
        "room_id": message.get("room_id"),
        "role": _normalize_role(message.get("role")),
        "content": message.get("content") or "",
        "created_at": message.get("created_at"),
    }


def _build_upload_file(uploaded_file: Any) -> tuple[str, bytes, str]:
    # Streamlit 업로드 파일을 requests multipart 형식으로 변환한다.
    """Build a multipart tuple from Streamlit's uploaded file object."""
    filename = getattr(uploaded_file, "name", "upload.bin")
    content_type = getattr(uploaded_file, "type", None) or "application/octet-stream"
    content = uploaded_file.getvalue()
    return filename, content, content_type


def fetch_chat_rooms_page(page: int = 1) -> dict[str, Any]:
    # 채팅방 목록을 페이지 단위로 조회한다.
    """Fetch a single chat-room page from the backend."""
    payload = _request_api(
        "GET",
        "/chat-rooms",
        params={"page": page, "size": ROOM_PAGE_SIZE},
    )
    return {
        "items": [_normalize_room(room) for room in payload.get("items", [])],
        "total": payload.get("total", 0),
        "page": payload.get("page", page),
        "size": payload.get("size", ROOM_PAGE_SIZE),
    }


def fetch_personas() -> list[str]:
    # 현재 최신 페르소나 목록을 조회한다.
    """Fetch the persona list from the backend source of truth."""
    payload = _request_api("GET", "/chat-rooms/personas")
    if not isinstance(payload, list):
        return []
    return [str(persona) for persona in payload if str(persona).strip()]


def fetch_all_messages(room_id: int) -> list[dict[str, Any]]:
    # 선택된 채팅방의 전체 메시지를 페이지를 따라 모두 모아온다.
    """Fetch every message page for a room and merge them into one list."""
    page = 1
    messages: list[dict[str, Any]] = []

    while True:
        payload = _request_api(
            "GET",
            f"/chat-rooms/{room_id}/messages",
            params={"page": page, "size": MESSAGE_PAGE_SIZE},
        )
        items = payload.get("items", [])
        messages.extend(items)

        total = payload.get("total", len(messages))
        if len(messages) >= total or not items:
            break
        page += 1

    return [_normalize_message(message) for message in messages]


def create_chat_room(member_id: int, title: str, persona: str) -> dict[str, Any]:
    # 새 채팅방을 생성하고 정규화된 결과를 반환한다.
    """Create a new chat room through the backend API."""
    room = _request_api(
        "POST",
        "/chat-rooms",
        json={"member_id": member_id, "title": title, "persona": persona},
    )
    return _normalize_room(room)


def delete_chat_room(room_id: int) -> None:
    # 특정 채팅방을 삭제한다.
    """Delete a chat room through the backend API."""
    _request_api("DELETE", f"/chat-rooms/{room_id}")


def send_ai_chat(room_id: int, message: str, uploaded_file: Any | None = None) -> dict[str, Any]:
    # 사용자 메시지와 첨부 파일을 AI 채팅 엔드포인트로 전송한다.
    """Send a user message and optional file to the AI chat endpoint."""
    files = None
    if uploaded_file is not None:
        files = {"file": _build_upload_file(uploaded_file)}

    return _request_api(
        "POST",
        f"/chat-rooms/{room_id}/AiChat",
        data={"message": message},
        files=files,
    )
