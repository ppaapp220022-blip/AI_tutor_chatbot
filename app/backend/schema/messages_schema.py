from datetime import datetime

from pydantic import BaseModel

from app.backend.model.messages import Role

# 요청
class MessageRequest(BaseModel):
    room_id: int
    role: Role
    content: str

# 응답
class MessageResponse(BaseModel):
    id: int
    room_id: int
    role: Role
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
