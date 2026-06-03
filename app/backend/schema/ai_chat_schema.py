from pydantic import BaseModel

# Ai 채팅 응답 스키마
class AiChatResponse(BaseModel):
    room_id: int
    user_message: str
    assistant_message: str
    uploaded_file_id: int | None = None
    file_name: str | None = None