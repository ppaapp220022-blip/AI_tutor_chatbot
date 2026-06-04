from datetime import datetime
from pydantic import BaseModel

from app.backend.schema.base_schema import PaginationResponse

# 채팅방 생성 요청 스키마
class ChatRoomCreateRequest(BaseModel):
    member_id: int
    title: str
    persona: str

# 채팅방 수정 요청 스키마
class ChatRoomUpdateRequest(BaseModel):
    title: str | None = None
    persona: str | None = None

# 채팅방 응답 스키마
class ChatRoomResponse(BaseModel):
    id: int
    member_id: int | None  # 회원 FK
    title: str | None  # 대화방 제목
    persona: str | None  # 페르소나
    created_at: datetime  # 생성일시

# 채팅방 설정 스키마
    class Config:  # ModelMapper (SqlAlchemy -> Pydantic)
        from_attributes = True

class ChatRoomPageResponse(PaginationResponse):
    items: list[ChatRoomResponse]