from datetime import datetime
from pydantic import ConfigDict
from app.backend.schema.base_schema import BaseSchema


class ChatRoomSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True)  # ModelMapper (SqlAlchemy -> Pydantic)

    id: int
    member_id: int | None  # 회원 FK
    title: str | None  # 대화방 제목
    persona: str | None  # 페르소나
    created_at: datetime  # 생성일시
