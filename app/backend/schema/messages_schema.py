from datetime import datetime

from pydantic import BaseModel

from app.backend.model.messages import Role
from app.backend.schema.base_schema import PaginationResponse

# 메시지 생성 요청 스키마
class MessageCreateRequest(BaseModel):
    role: Role
    content: str

# 메시지 수정 요청 스키마
class MessageUpdateRequest(BaseModel):
    content: str

# 메시지 응답 스키마
class MessageResponse(BaseModel):
    id: int
    room_id: int
    role: Role
    content: str
    created_at: datetime

# 메시지 설정 스키마
    class Config: # ModelMapper (SqlAlchemy -> Pydantic)
        from_attributes = True

class MessagePageResponse(PaginationResponse):
    items: list[MessageResponse]