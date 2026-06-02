from datetime import datetime, timezone, timedelta
from sqlalchemy import Integer, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum
from app.backend.database import Base

KST = timezone(timedelta(hours=9))


class Role(enum.Enum):
    USER = 'user'
    Assistant = 'assistant'


class Messages(Base):
    __tablename__ = 'messages'
    __table_args__ = {'comment': '메시지'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='메시지 고유 번호')
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey("chat_rooms.id"), nullable=True, comment='대화방 FK')  # FK
    role: Mapped[Role] = mapped_column(
        Enum(Role, name="message_role", values_callable=lambda enum_cls: [item.value for item in enum_cls]),
        nullable=True,
        comment='user or assistant'
    )
    content: Mapped[str] = mapped_column(Text, nullable=True, comment='내용')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(KST), comment='메시지 전송 일시')

    # FK (자식)
    chat_room = relationship('ChatRoom', back_populates='messages')
