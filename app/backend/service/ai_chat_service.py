from pathlib import Path
from typing import Literal

from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from app.backend.model.messages import Messages
from app.backend.model.messages import Role
from app.backend.repository.chat_room_repository import find_chat_room
from app.backend.service.ai_client_service import request_chat_completion
from app.backend.service.file_parser_service import extract_text_from_file
from app.backend.service.messages_service import (
    get_all_messages_service,
    post_messages_service,
)
from app.backend.service.uploaded_files_service import save_upload_file_service

SYSTEM_PROMPT = (
    "당신은 업로드된 PDF 문서와 대화 문맥을 바탕으로 답변하는 AI 튜터입니다. "
    "당신은 전문적인 지식을 사용자가 이해하기 쉽게 설명해야 하고, "
    "사용자가 원하는 지식을 습득하기 위해 최선의 노력을 해야합니다."
    "필요하다면 추가적인 질문을 계속 사용자에게 요구하세요."
)

MAX_FILE_CONTEXT_LENGTH = 12000
MAX_HISTORY_COUNT = 20


def _to_openai_role(role: Role) -> Literal["user", "assistant"]: # 반환값은 user, assistent 만 가질 수 있도록 명시
    if role == Role.USER:
        return "user"
    return "assistant"


def build_openai_messages(history: list[Messages], user_message: str, file_text: str = "") -> list[ChatCompletionMessageParam]: # OpenAI에서 채팅타입을 명시 해줌
    messages: list[ChatCompletionMessageParam] = []

    system_message: ChatCompletionSystemMessageParam = {
        "role": "system",
        "content": SYSTEM_PROMPT,
    }
    messages.append(system_message)

    if file_text:
        file_message: ChatCompletionSystemMessageParam = {
            "role": "system",
            "content": f"[업로드된 PDF 문서 내용]\n{file_text[:MAX_FILE_CONTEXT_LENGTH]}",
        }
        messages.append(file_message)

    for history_message in history[-MAX_HISTORY_COUNT:]:
        if _to_openai_role(history_message.role) == "user":
            user_chat_message: ChatCompletionUserMessageParam = {
                "role": "user",
                "content": history_message.content,
            }
            messages.append(user_chat_message)
        else:
            assistant_chat_message: ChatCompletionAssistantMessageParam = {
                "role": "assistant",
                "content": history_message.content,
            }
            messages.append(assistant_chat_message)

    user_message_param: ChatCompletionUserMessageParam = {
        "role": "user",
        "content": user_message,
    }
    messages.append(user_message_param)
    return messages


def handle_chat_request_service(db, room_id: int, user_message: str, upload_file=None) -> dict:
    if not room_id:
        raise ValueError("채팅방을 확인할 수 없습니다.")

    if not user_message or not user_message.strip():
        raise ValueError("사용자 메시지가 비어 있습니다.")

    room = find_chat_room(db, room_id)
    if not room:
        raise ValueError("채팅방이 존재하지 않습니다.")

    uploaded = None
    file_text = ""

    try:
        if upload_file is not None:
            uploaded = save_upload_file_service(db, room_id, upload_file, commit=False)
            file_text = extract_text_from_file(uploaded.file_path)

        history = get_all_messages_service(db, room_id)

        openai_messages = build_openai_messages(history, user_message.strip(), file_text)

        post_messages_service(db, room_id, Role.USER, user_message.strip(), commit=False)

        assistant_message = request_chat_completion(openai_messages)

        if not assistant_message:
            raise ValueError("AI 응답을 생성하지 못했습니다.")

        post_messages_service(db, room_id, Role.Assistant, assistant_message, commit=False)
        db.commit()
    except Exception:
        db.rollback()
        if uploaded and uploaded.file_path:
            uploaded_path = Path(uploaded.file_path)
            if uploaded_path.exists():
                uploaded_path.unlink()
            parent_dir = uploaded_path.parent
            if parent_dir.exists() and not any(parent_dir.iterdir()):
                parent_dir.rmdir()
        raise

    return {
        "room_id": room_id,
        "user_message": user_message.strip(),
        "assistant_message": assistant_message,
        "uploaded_file_id": uploaded.id if uploaded else None,
        "file_name": uploaded.file_name if uploaded else None,
    }
