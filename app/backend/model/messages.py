from datetime import datetime, timezone, timedelta
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
import enum
from sqlalchemy.orm import relationship

from app.backend.database import Base

KST = timezone(timedelta(hours=9))

class Role(enum.Enum):
    USER = 'USER'
    Assistant = 'ASSISTANT'

class Messages(Base):
    __tablename__ = 'messages'
    __table_args__ = {'comment' : '메시지'}

    id: int = Column(Integer, primary_key=True, autoincrement=True, comment='메시지 고유 번호')
    room_id: int = Column(Integer, nullable=True, comment='대화방 FK') # FK
    role: Role = Column(Enum(Role), nullable=True, comment='user or assistant')
    content: str = Column(Text, nullable=True, comment='내용')
    created_at: datetime = Column(DateTime, default=lambda: datetime.now(KST), comment='메시지 전송 일시')