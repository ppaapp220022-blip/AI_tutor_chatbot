from datetime import datetime
from pydantic import BaseModel


class ChatRoomSchema(BaseModel):
    id: int
    member_id: int | None # 회원 FK
    title: str | None # 대화방 제목
    persona: str | None # 페르소나
    created_at: datetime # 생성일시

    class Config: # ModelMapper (SqlAlchemy -> Pydantic)
        from_attributes = True